import aiosqlite
from logging import *
from services.config import Config
from typing import Any

class Database:
    INIT_TABLES = """
    CREATE TABLE IF NOT EXISTS guilds (
        guild_id INTEGER PRIMARY KEY,
        category_id INTEGER,
        text_channels_limit INTEGER DEFAULT 20,
        text_channels_delay INTEGER DEFAULT 30,
        text_channels_prefix TEXT DEFAULT 'group-',
        text_channels_user_limit INTEGER DEFAULT 5,
        text_channels_enabled INTEGER DEFAULT 1,
        ticket_category_id INTEGER,
        ticket_role_id INTEGER
    );
    CREATE TABLE IF NOT EXISTS temp_channels (
        channel_id INTEGER PRIMARY KEY,
        guild_id INTEGER NOT NULL,
        members TEXT NOT NULL,
        private TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS tickets (
        channel_id INTEGER PRIMARY KEY,
        guild_id INTEGER NOT NULL,
        member INTEGER NOT NULL
    );
    """

    GUILDS_KEYS = (
        "guild_id",
        "category_id",
        "text_channels_limit",
        "text_channels_delay",
        "text_channels_prefix",
        "text_channels_user_limit",
        "text_channels_enabled",
        "ticket_category_id",
        "ticket_role_id"
    )

    @staticmethod
    async def init() -> bool:
        PATH = Config["paths"]["database"]
        assert PATH

        async with aiosqlite.connect(PATH) as db:
            db: aiosqlite.Connection = db
            await db.executescript(Database.INIT_TABLES)
            await db.commit()
        info("data base inited")
    
    @staticmethod
    async def test() -> tuple[list]:
        PATH = Config["paths"]["database"]
        assert PATH

        async with aiosqlite.connect(PATH) as db:
            db: aiosqlite.Connection = db
            cursor = await db.execute("SELECT * FROM guilds")

            return await cursor.fetchall()
        
    class Guilds:
        @staticmethod
        async def get_configs(guild_id: int) -> (Any | dict):
            PATH = Config["paths"]["database"]

            async with aiosqlite.connect(PATH) as db:
                db: aiosqlite.Connection = db
                cursor = await db.execute("SELECT * FROM guilds WHERE guild_id=?", (guild_id,))
                if result := await cursor.fetchone():
                    result = dict(zip(Database.GUILDS_KEYS, result)) # Fetchone returns (data1, data2, ..., dataN)
                else:
                    result = None
            return result

        @staticmethod
        async def ids() -> (Any | list):
            PATH = Config["paths"]["database"]
            assert PATH

            async with aiosqlite.connect(PATH) as db:
                db: aiosqlite.Connection = db
                cursor = await db.execute("SELECT guild_id FROM guilds")
                if result := await cursor.fetchall():
                    result = [r[0] for r in result] # Fetchall returns [(id,), (id2,), ..., (idN,)]
                else:
                    result = None
            return result
