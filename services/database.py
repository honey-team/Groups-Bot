import asyncpg
import asyncio

async def bd_connect() -> asyncpg.Connection:
    return await asyncpg.connect("postgresql://postgres@localhost/groupsbot")
async def get_groups(guild_id: int) -> dict:
    conn = await bd_connect()
    result = await conn.fetch(f"SELECT * FROM groupsTable WHERE guild_id = $1", guild_id)
    await conn.close()
    return [dict(row) for row in result][0]



async def create_group(guild_id: int, l: list):
    conn = await bd_connect()
    await conn.execute(f"INSERT INTO groupsTable (category_id, special_roles, lang) VALUES ($2, $3, $4) where guild_id = $1", guild_id, l[0], l[1], l[2], l[3])
    await conn.close()