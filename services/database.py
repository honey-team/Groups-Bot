import aiosqlite, json
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
        text_channels_enabled INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS temp_channels (
        channel_id INTEGER PRIMARY KEY,
        guild_id INTEGER NOT NULL,
        members TEXT NOT NULL,
        owners TEXT NOT NULL,
        private INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        temp_channels_count INTEGER NOT NULL,
        last_temp_channel_created TEXT NOT NULL
    )
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
    GROUPS_KEYS = (
        "channel_id",
        "guild_id",
        "members",
        "owners",
        "private"
    )
    USER_KEYS = (
        "user_id",
        "temp_channels_count",
        "last_temp_channel_created" 
    )

    @staticmethod
    async def init() -> bool:
        PATH = Config["paths"]["database"]

        async with aiosqlite.connect(PATH) as db:
            db: aiosqlite.Connection = db
            await db.executescript(Database.INIT_TABLES)
            await db.commit()
        info("data base inited")
    
    @staticmethod
    async def test() -> tuple[list]:
        PATH = Config["paths"]["database"]

        async with aiosqlite.connect(PATH) as db:
            db: aiosqlite.Connection = db
            cursor = await db.execute("SELECT * FROM guilds")

            return await cursor.fetchall()
        
    class Guilds:
        @staticmethod
        async def get_config(db: aiosqlite.Connection, guild_id: int) -> (None | dict):
            if result := await (await db.execute("SELECT * FROM guilds WHERE guild_id=?", (guild_id,))).fetchall():
                return Database.Json.parse(dict(zip(Database.GUILDS_KEYS, result[0]))) # Fetchone returns (data1, data2, ..., dataN)
            else:
                return None

        @staticmethod
        async def ids(db: aiosqlite.Connection) -> (Any | tuple):
            if result := await (await db.execute("SELECT (guild_id) FROM guilds")).fetchall():
                return result[0]
            else:
                return None
    
    class TempChannels:
        @staticmethod
        async def get_config(db: aiosqlite.Connection, channel_id: int) -> (None | dict):
            if result := await (await db.execute("SELECT * FROM temp_channels WHERE channel_id=?", (channel_id,))).fetchall():
                return Database.Json.parse(dict(zip(Database.GROUPS_KEYS, result[0]))) # Fetchone returns (data1, data2, ..., dataN)
            else:
                return None
        
        @staticmethod
        async def count(db: aiosqlite.Connection, guild_id: int = None) -> (None | dict):
            if guild_id:
                if result := await (await db.execute("SELECT * FROM temp_channels WHERE guild_id=?", (guild_id,))).fetchall():
                    return len(result)
                else:
                    return None
            else:
                if result := await (await db.execute("SELECT * FROM temp_channels")).fetchall():
                    return len(result)
                else:
                    return None

        @staticmethod
        async def ids(db: aiosqlite.Connection) -> (Any | tuple):
            if result := await (await db.execute("SELECT (channel_id) FROM temp_channels")).fetchall():
                return result[0]
            else:
                return None
    
    class Users:
        @staticmethod
        async def get_config(db: aiosqlite.Connection, user_id: int) -> (None | dict):
            if result := await (await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))).fetchall():
                return Database.Json.parse(dict(zip(Database.USER_KEYS, result[0]))) # Fetchone returns (data1, data2, ..., dataN)
            else:
                return None
        
        @staticmethod
        async def ids(db: aiosqlite.Connection) -> (Any | tuple):
            if result := await (await db.execute("SELECT (user_id) FROM users")).fetchall():
                return result[0]
            else:
                return None
    
    class Json:
        @staticmethod
        def parse(values: dict) -> dict:
            for key, value in values.items():
                if key in [
                    "members",
                    "owners"
                ]:
                    # Parse to python var
                    values[key] = json.loads(value)
            return values