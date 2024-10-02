import aiosqlite
from logging import *
from services.config import Config
from typing import Any

class Database:
    INIT_TABLES = """
    CREATE TABLE IF NOT EXISTS guilds (
        guild_id INTEGER PRIMARY KEY,
        category_id INTEGER,
        text_channels_limit INTEGER,
        text_channels_delay INTEGER,
        text_channels_prefix INTEGER,
        text_channels_user_limit INTEGER,
        text_channels_enabled TEXT
    );
    CREATE TABLE IF NOT EXISTS temp_channels (
        channel_id INTEGER PRIMARY KEY,
        guild_id INTEGER,
        members TEXT,
        private TEXT
    );
    """

    GUILDS_KEYS = (
        "guild_id",
        "category_id",
        "text_channels_limit",
        "text_channels_delay",
        "text_channels_prefix",
        "text_channels_user_limit",
        "text_channels_enabled"
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
            assert PATH
            assert guild_id

            data = {
                "guild_id":guild_id
            }

            async with aiosqlite.connect(PATH) as db:
                db: aiosqlite.Connection = db
                cursor = await db.execute("SELECT * FROM guilds WHERE guild_id=:guild_id", data)
                if result := await cursor.fetchall():
                    result = dict(zip(Database.GUILDS_KEYS, result[0])) # Fetchall returns [(data1, data2, ..., dataN)]
                else:
                    result = None
            return result

        @staticmethod
        async def ids() -> (Any | dict):
            PATH = Config["paths"]["database"]
            assert PATH

            async with aiosqlite.connect(PATH) as db:
                db: aiosqlite.Connection = db
                cursor = await db.execute("SELECT (guild_id) FROM guilds")
                if result := await cursor.fetchall():
                    result = result[0] # Fetchall returns [(data1, data2, ..., dataN)]
                else:
                    result = None
            return result
