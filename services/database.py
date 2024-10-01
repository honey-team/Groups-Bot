import aiosqlite
from logging import *
from services.config import Config
from typing import Any

class Database:
    INIT_TABLES = """
    CREATE TABLE IF NOT EXISTS guilds (
        guild_id INTAGER PRIMARY KEY UNIQUE,
        category_id INTAGER DEFAULT NULL,
        text_channels_limit INTAGER DEFAULT NULL,
        text_channels_delay INTAGER DEFAULT NULL,
        text_channels_prefix INTAGER DEFAULT NULL,
        text_channels_user_limit INTAGER DEFAULT NULL,
        text_channels_enabled TEXT DEFAULT NULL
    );
    CREATE TABLE IF NOT EXISTS temp_channels (
        channel_id INTAGER PRIMARY KEY,
        guild_id INTAGER DEFAULT NULL UNIQUE,
        members TEXT DEFAULT NULL,
        private TEXT DEFAULT NULL
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
        
    @staticmethod
    async def get_guild_configs(guild_id: int) -> (Any | dict):
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
