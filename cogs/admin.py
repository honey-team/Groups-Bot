import disnake, aiosqlite
from aiosqlite import Connection
from disnake.ext import commands
from services.database import *
from services.embeds import *
from services.config import Config
from services.interfaces import AdminCommandsInterface

class AdminCog(commands.Cog, AdminCommandsInterface):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.debug = True
    
    @commands.slash_command(
        name="set-groups-category"
    )
    @commands.has_guild_permissions(administrator=True)
    async def set_groups_category(
        self,
        inter: disnake.ApplicationCommandInteraction,
        category: disnake.CategoryChannel
    ):
        if category in inter.guild.categories:
            DB_PATH = Config["paths"]["database"]

            db = await aiosqlite.connect(DB_PATH)
            # check values
            if category in inter.guild.categories:
                # get old config
                if guild_config := await Database.Guilds.get_config(db, inter.guild_id):
                    guild_config["groups_category_id"] = category.id
                else:
                    guild_config = {
                        "groups_enabled":True,
                        "groups_limit":None,
                        "groups_category_id":category.id
                    }
                await Database.Guilds.set_config(db, inter.guild_id, guild_config)
                await db.commit()
                await inter.response.send_message(embed=Success(description="Changed groups category id. New value: <#{0}>".format(category.id)))
            await db.close()
        else:
            await inter.response.send_message(embed=Error(description="Unknown category"))
    
    @commands.slash_command(
        name="set-groups-enabled"
    )
    @commands.has_guild_permissions(administrator=True)
    async def set_groups_enabled(
        self,
        inter: disnake.ApplicationCommandInteraction,
        enabled: bool
    ):
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            # get old config
            if guild_config := await Database.Guilds.get_config(db, inter.guild_id):
                guild_config["groups_enabled"] = enabled
            else:
                guild_config = {
                    "groups_enabled":enabled,
                    "groups_limit":10,
                    "groups_category_id":None
                }
            await Database.Guilds.set_config(db, inter.guild_id, guild_config)
            await db.commit()
            await inter.response.send_message(embed=Success(description="Changed groups enabled. New value: `{0}`".format(enabled)))

    @commands.slash_command(
        name="set-groups-limit"
    )
    @commands.has_guild_permissions(administrator=True)
    async def set_groups_limit(
        self,
        inter: disnake.ApplicationCommandInteraction,
        limit: int
    ):
        if limit > 0:
            DB_PATH = Config["paths"]["database"]

            async with aiosqlite.connect(DB_PATH) as db:
                # get old config
                if guild_config := await Database.Guilds.get_config(db, inter.guild_id):
                    guild_config["groups_limit"] = limit
                else:
                    guild_config = {
                        "groups_enabled":enabled,
                        "groups_limit":limit,
                        "groups_category_id":category.id
                    }
                await Database.Guilds.set_config(db, inter.guild_id, guild_config)
                await db.commit()
                await inter.response.send_message(embed=Success(description="Changed groups enabled. New value: `{0}`".format(limit)))
        else:
            await inter.response.send_message(embed=Error(description="Invalid value: `{0}`".format(limit)))

    @commands.slash_command(
        name="guild-config"
    )
    @commands.has_guild_permissions(administrator=True)
    async def guild_config(self, inter: disnake.ApplicationCommandInteraction):
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            if guild_config := await Database.Guilds.get_config(db, inter.guild_id):
                embed = Info(description="**Guild configurations**")
                for key, value in guild_config.items():
                    embed.add_field(f"`{key}`", f"`{value}`", inline=False)
                await inter.response.send_message(embed=embed)
            else:
                guild_config = {}
                await Database.Guilds.set_config(db, inter.guild_id, guild_config)
                await db.commit()

def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))
