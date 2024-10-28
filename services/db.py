from __future__ import annotations
import aiosqlite, typing, settings

INIT_TABLES = """
CREATE TABLE IF NOT EXISTS guilds (
    guild_id INTEGER PRIMARY KEY,
    groups_category_id INTEGER,
    groups_count_limit INTEGER,
    groups_enabled INTEGER
);
"""

DEFAULT_VALUES = (
    None,
    10,
    True
)

async def create_tables():
    async with aiosqlite.connect(settings.DB_PATH) as con:
        await con.executescript(INIT_TABLES)
        await con.commit()

def format(list: list) -> GuildDict:
    return GuildDict(zip(
        (
            "groups_category_id",
            "groups_count_limit",
            "groups_enabled"
        ),
        list
    ))

class GuildDict(typing.TypedDict):
    groups_category_id: int
    groups_count_limit: int
    grouns_enabled: bool
