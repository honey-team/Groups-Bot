import disnake
from disnake.ext import commands
from os import path
import json

defaults: dict = json.load(open(path.join(path.dirname(__file__), "en.json"), encoding="utf-8"))
russian: dict = json.load(open(path.join(path.dirname(__file__), "ru.json"), encoding="utf-8"))

def localised_command(
    *,
    key: str=None,
    **kwargs
):
    """
    A shortcut decorator for localizing commands.

    Arguments:
    key: str=None - Name of command for lookup in localization file
    """
    def decorator(func):
        d = defaults
        ru = russian
        k = key.upper() if key is not None else func.__name__.upper()
        name = f'{k}_COMMAND_NAME'
        description = f'{k}_COMMAND_DOC'
        return commands.slash_command(
            name=disnake.Localised(d.get(name), data={disnake.Locale.ru: ru.get(name)}) if name in ru else d.get(name),
            description=disnake.Localised(d.get(description), data={disnake.Locale.ru: ru.get(description)}) if description in ru else d.get(description),
            **kwargs)(func)

    return decorator