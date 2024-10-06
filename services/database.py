from __future__ import annotations
import aiosqlite, json
from services.config import Config
from typing import Any

class Database:
    INIT_TABLES = """
    CREATE TABLE IF NOT EXISTS guilds (
        id INTEGER PRIMARY KEY,
        guild_config TEXT NOT NULL
    );
    """

    @staticmethod
    async def init() -> None:
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            await db.executescript(Database.INIT_TABLES)
            await db.commit()
    
    class Guilds:
        @staticmethod
        async def get_config(db: aiosqlite.Connection, guild_id: int) -> (None | dict):
            if cursor := await (await db.execute(
                "SELECT (guild_config) FROM guilds WHERE id=?",
                (guild_id, )
            )).fetchall():
                return json.loads(cursor[0][0]) # fetchall return `tuple[list]`
            else:
                return None
        
        @staticmethod
        async def set_config(
            db: aiosqlite.Connection,
            guild_id: int,
            guild_config: dict
        ) -> None:
            guild_id = int(guild_id)
            guild_config = json.dumps(guild_config)
            await db.execute("INSERT OR REPLACE INTO guilds VALUES (?, ?)", (guild_id, guild_config))

__all__ = (
    "Database",
)
