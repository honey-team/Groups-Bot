import disnake, datetime, aiosqlite
from logging import *
from disnake.ext import commands
from services.interfaces import AdminCommandsInterface
from services.config import Config
from services.embeds import *
from services.database import Database

class AdminCog(commands.Cog, AdminCommandsInterface):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.debug = True

    @commands.slash_command(
        name="change_groups_category"
    )
    @commands.has_permissions(administrator=True)
    async def temp_text_channels_category(
        self,
        inter: disnake.ApplicationCommandInteraction,
        category: disnake.CategoryChannel
    ):
        DB_PATH = Config["paths"]["database"]

        data = {
            "guild_id":inter.guild_id,
            "category_id":category.id
        }
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT (guild_id) FROM guilds")
            guilds_ids = [t[0] for t in (await cursor.fetchall())]
            if data["guild_id"] in guilds_ids:
                await db.execute("UPDATE guilds SET category_id=:category_id WHERE guild_id=:guild_id", data)
            else:
                await db.execute("INSERT OR REPLACE INTO guilds (guild_id, category_id) VALUES (:guild_id, :category_id)", data)
            await db.commit()
        # Send response
        await inter.response.send_message(
            embed=Success(description="New value of groups category. ID: **{0}**".format(data["category_id"])),
            ephemeral=not self.debug
        )

    @commands.slash_command(
        name="change_groups_delay"
    )
    @commands.has_permissions(administrator=True)
    async def change_temp_channels_delay(
        self,
        inter: disnake.ApplicationCommandInteraction,
        delay: int,
    ):
        if delay > 0 and delay <= 3600:
            DB_PATH = Config["paths"]["database"]

            data = {
                "guild_id":inter.guild_id,
                "text_channels_delay":delay
            }
            async with aiosqlite.connect(DB_PATH) as db:
                cursor = await db.execute("SELECT (guild_id) FROM guilds")
                guilds_ids = [t[0] for t in (await cursor.fetchall())]
                if data["guild_id"] in guilds_ids:
                    await db.execute("UPDATE guilds SET text_channels_delay=:text_channels_delay WHERE guild_id=:guild_id", data)
                else:
                    await db.execute("INSERT OR REPLACE INTO guilds (guild_id, text_channels_delay) VALUES (:guild_id, :text_channels_delay)", data)
                await db.commit()
            # Send response
            await inter.response.send_message(
                embed=Success(description="New text channels delay: **{0}**".format(data["text_channels_delay"])),
                ephemeral=not self.debug
            )
        else:
            await inter.response.send_message(
                embed=Error(description="Max value of delay is 3600"),
                ephemeral=not self.debug
            )
    
    @commands.slash_command(
        name="change_groups_prefix"
    )
    @commands.has_permissions(administrator=True)
    async def change_temp_text_channels_prefix(
        self,
        inter: disnake.ApplicationCommandInteraction,
        prefix: str,
    ):
        if len(prefix) <= 10:
            DB_PATH = Config["paths"]["database"]

            data = {
                "guild_id":inter.guild_id,
                "text_channels_prefix":prefix
            }
            async with aiosqlite.connect(DB_PATH) as db:
                cursor = await db.execute("SELECT (guild_id) FROM guilds")
                guilds_ids = [t[0] for t in (await cursor.fetchall())]
                if data["guild_id"] in guilds_ids:
                    await db.execute("UPDATE guilds SET text_channels_prefix=:text_channels_prefix WHERE guild_id=:guild_id", data)
                else:
                    await db.execute("INSERT OR REPLACE INTO guilds (guild_id, text_channels_prefix) VALUES (:guild_id, :text_channels_prefix)", data)
                await db.commit()
            # Send response
            await inter.response.send_message(
                embed=Success(description="New text channels prefix: **{0}**".format(data["text_channels_prefix"])),
                ephemeral=not self.debug
            )
        else:
            await inter.response.send_message(
                embed=Error(description="Max len of prefix is 10"),
                ephemeral=not self.debug
            )

    @commands.slash_command(
        name="change_groups_user_limit"
    )
    @commands.has_permissions(administrator=True)
    async def change_user_temp_channels_limit(
        self,
        inter: disnake.ApplicationCommandInteraction,
        limit: int,
    ):
        DB_PATH = Config["paths"]["database"]

        data = {
            "guild_id":inter.guild_id,
            "text_channels_limit":limit
        }
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT (guild_id) FROM guilds")
            guilds_ids = [t[0] for t in (await cursor.fetchall())]
            if data["guild_id"] in guilds_ids:
                await db.execute("UPDATE guilds SET text_channels_limit=:text_channels_limit WHERE guild_id=:guild_id", data)
            else:
                await db.execute("INSERT OR REPLACE INTO guilds (guild_id, text_channels_limit) VALUES (:guild_id, :text_channels_limit)", data)
            await db.commit()
        # Send response
        await inter.response.send_message(
            embed=Success(description="New text channels user limit: **{0}**".format(data["text_channels_limit"])),
            ephemeral=not self.debug
        )

    @commands.slash_command(
        name="groups_enabled"
    )
    @commands.has_permissions(administrator=True)
    async def temp_text_channels_enabled(
        self,
        inter: disnake.ApplicationCommandInteraction,
        enabled: bool,
    ):
        DB_PATH = Config["paths"]["database"]

        data = {
            "guild_id":inter.guild_id,
            "text_channels_enabled":enabled
        }
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT (guild_id) FROM guilds")
            guilds_ids = [t[0] for t in (await cursor.fetchall())]
            if data["guild_id"] in guilds_ids:
                await db.execute("UPDATE guilds SET text_channels_enabled=:text_channels_enabled WHERE guild_id=:guild_id", data)
            else:
                await db.execute("INSERT OR REPLACE INTO guilds (guild_id, text_channels_enabled) VALUES (:guild_id, :text_channels_enabled)", data)
            await db.commit()
        # Send response
        await inter.response.send_message(
            embed=Success(description="Text channels enabled: **{0}**".format(data["text_channels_enabled"])),
            ephemeral=not self.debug
        )
    
    @commands.slash_command(
        name="change_groups_limit"
    )
    @commands.has_permissions(administrator=True)
    async def change_temp_channels_limit(
        self,
        inter: disnake.ApplicationCommandInteraction,
        limit: int,
    ):
        DB_PATH = Config["paths"]["database"]

        data = {
            "guild_id":inter.guild_id,
            "text_channels_limit":limit
        }
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT (guild_id) FROM guilds")
            guilds_ids = [t[0] for t in (await cursor.fetchall())]
            if data["guild_id"] in guilds_ids:
                await db.execute("UPDATE guilds SET text_channels_limit=:text_channels_limit WHERE guild_id=:guild_id", data)
            else:
                await db.execute("INSERT OR REPLACE INTO guilds (guild_id, text_channels_limit) VALUES (:guild_id, :text_channels_limit)", data)
            await db.commit()
        # Send response
        await inter.response.send_message(
            embed=Success(description="New groups limit: **{0}**".format(data["text_channels_limit"])),
            ephemeral=not self.debug
        )

    @commands.slash_command(
        name="guild_configs"
    )
    @commands.has_permissions(administrator=True)
    async def get_guild_configs(self, inter: disnake.ApplicationCommandInteraction):
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            # Get guilds ids
            guilds_ids = await Database.Guilds.ids(db)
            
            if inter.guild_id not in guilds_ids:
                # Insert guild to guilds
                await db.execute("INSERT INTO guilds (guild_id) VALUES (?)", (inter.guild_id,))
                await db.commit()
            # Get guild configs
            guild_configs = await Database.Guilds.get_config(db, inter.guild_id)
            # Format and send
            embed = Info(description="**Guild configurations:**")
            for key, value in guild_configs.items():
                embed.add_field(
                    name=f"`{key}`",
                    value=f"`{value}`",
                    inline=False
                )
            await inter.response.send_message(embed=embed, ephemeral=not self.debug)

    @commands.slash_command(
        name="group-config"
    )
    @commands.has_permissions(administrator=True)
    async def get_group_configs(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            group_configs = await Database.TempChannels.get_config(db, channel.id)
            group_configs = Database.Json.parse(group_configs)
            # Format and send
            embed = Info(description="**Group configurations:**")
            for key, value in group_configs.items():
                embed.add_field(
                    name=f"`{key}`",
                    value=f"`{value}`",
                    inline=False
                )
            await inter.response.send_message(embed=embed, ephemeral=not self.debug)
    
    @commands.slash_command(
        name="delete_group"
    )
    @commands.has_guild_permissions(manage_channels=True)
    async def delete_temp_channel(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ): # It is not working yet
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            guilds_ids = [g[0] for g in (await (await db.execute("SELECT (guild_id) FROM guilds")).fetchall())]
            print(guilds_ids)
            guild_configs = await (await db.execute("SELECT * FROM guilds WHERE guild_id=?", (inter.guild_id,)))

        if inter.guild_id in guilds_ids:
            guild_configs = Database.Guilds.get_config(inter.guild_id)
            if category_id := guild_configs["category_id"]:
                if channel.category_id == category_id:
                    pass # Delete channel
                    await inter.response.send_message(embed=Success(description="Succes deleted channel. ID: **{0}**".format(channel.id)))
                else:
                    await inter.response.send_message(embed=Error(description="Channel <#{0}> is not a group".format(channel.id)))
            else:
                await inter.response.send_message(embed=Error(description="Use `change_groups_category` before use it again"))
        else:
            await inter.response.send_message(embed=Error(description="Use `change_groups_category` before use it again"))

def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))
