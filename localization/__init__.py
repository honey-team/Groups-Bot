import disnake
from disnake.ext import commands
from os import path
import json
import collections
from typing import Coroutine, Dict, Any, Callable, Optional, Sequence
import asyncio

defaults: dict = json.load(open(path.join(path.dirname(__file__), "en.json"), encoding="utf-8"))
russian: dict = json.load(open(path.join(path.dirname(__file__), "ru.json"), encoding="utf-8"))
for i in defaults.items():
    if i[0] not in russian:
        russian[i[0]] = i[1]

class CaseInsensitiveDict(collections.abc.MutableMapping): # this class is stolen from requests
    """
    A case-insensitive ``dict``-like object.

    Implements all methods and operations of
    ``collections.MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.

    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive:

        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.

    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.

    """
    def __init__(self, data=None, **kwargs):
        self._store = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return (
            (lowerkey, keyval[1])
            for (lowerkey, keyval)
            in self._store.items()
        )

    def __eq__(self, other):
        if isinstance(other, collections.Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, dict(self.items()))
    
# class ends here

def get_localised_string(
    key: str, 
    locale: disnake.Locale
):
    """
    A command for getting localized text from localization file.

    Arguments:
    key: str - Name of command for lookup in localization file
    locale: disnake.Locale - Locale for getting localized text
    """
    key = key.upper()
    if locale == disnake.Locale.ru:
        d = russian
    else:
        d = defaults
    return d.get(key)

def get_command_data(
    key: str, 
    locale: disnake.Locale
):
    """
    A command for getting localized text from localization file.

    Arguments:
    key: str - Name of command for lookup in localization file
    locale: disnake.Locale - Locale for getting localized text
    """
    key = key.upper()
    if locale == disnake.Locale.ru:
        d = russian
    else:
        d = defaults
    return CaseInsensitiveDict({x[len(key) + 9:]: val for x, val in d.items() if x.startswith(key)})

class LocalisedCommand(commands.InvokableSlashCommand):
    def sub_command(self, key: str = None, options: list | None = None, connectors: dict | None = None, extras: Dict[str, Any] | None = None, **kwargs) -> Callable[[Callable[..., Coroutine[Any, Any, Any]]], commands.SubCommand]:
        sc = super().sub_command
        def decorator(func):
            d = defaults
            ru = russian
            k = key.upper() if key is not None else func.__name__.upper()
            name = f'{k}_COMMAND_NAME'
            description = f'{k}_COMMAND_DOC'
            return sc(
                disnake.Localised(d.get(name), data={disnake.Locale.ru: ru.get(name)}) if name in ru else d.get(name),
                disnake.Localised(d.get(description), data={disnake.Locale.ru: ru.get(description)}) if description in ru else d.get(description),
                options, connectors, extras, **kwargs)(func)
        return decorator

def localised_command(
    key: str=None,
    dm_permission: Optional[bool] = None,
    default_member_permissions = None,
    nsfw: Optional[bool] = None,
    options = None,
    guild_ids: Optional[Sequence[int]] = None,
    connectors: Optional[Dict[str, str]] = None,
    auto_sync: Optional[bool] = None,
    extras: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """
    A shortcut decorator for localizing commands.

    Arguments:
    key: str=None - Name of command for lookup in localization file
    """

    def decorator(func) -> LocalisedCommand:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f"<{func.__qualname__}> must be a coroutine function")
        if hasattr(func, "__command_flag__"):
            raise TypeError("Callback is already a command.")
        if guild_ids and not all(isinstance(guild_id, int) for guild_id in guild_ids):
            raise ValueError("guild_ids must be a sequence of int.")
        d = defaults
        ru = russian
        k = key.upper() if key is not None else func.__name__.upper()
        name = f'{k}_COMMAND_NAME'
        description = f'{k}_COMMAND_DOC'
        return LocalisedCommand(
            func,
            name=disnake.Localised(d.get(name), data={disnake.Locale.ru: ru.get(name)}) if name in ru else d.get(name),
            description=disnake.Localised(d.get(description), data={disnake.Locale.ru: ru.get(description)}) if description in ru else d.get(description),
            options=options,
            dm_permission=dm_permission,
            default_member_permissions=default_member_permissions,
            nsfw=nsfw,
            guild_ids=guild_ids,
            connectors=connectors,
            auto_sync=auto_sync,
            extras=extras,
            **kwargs,
        )

    return decorator