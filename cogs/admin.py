from __future__ import annotations
from disnake.ext import commands
from services import db, embeds, interfaces
import aiosqlite, settings, disnake

class AdminGroupsCog(commands.Cog, interfaces.AdminGroupsCommandsInterface):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot
    
    @commands.slash_command(
        name="setup",
        description="Setup bot for this guild"
    )
    @commands.has_permissions(administrator=True)
    async def setup(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):
        async with aiosqlite.connect(settings.DB_PATH) as con:
            await con.execute(
                "INSERT OR REPLACE INTO guilds VALUES (?, ?, ?, ?)",
                (inter.guild_id,) + db.DEFAULT_VALUES
            )
            await con.commit()
        await inter.response.send_message(embed=embeds.Success(description="Successfully."), ephemeral=True)

    @commands.slash_command(
        name="set-groups-category",
        description="Returns bot latency."
    )
    @commands.has_permissions(administrator=True)
    async def set_groups_category(
        self,
        inter: disnake.ApplicationCommandInteraction,
        category: disnake.CategoryChannel
    ):
        async with aiosqlite.connect(settings.DB_PATH) as con:
            await con.execute(
                "UPDATE guilds SET groups_category_id=? WHERE guild_id=?",
                (category.id, inter.guild_id)
            )
            await con.commit()
        await inter.response.send_message(embed=embeds.Success(description="groups_category_id new value: <#{0}>".format(category.id)), ephemeral=True)
    
    @commands.slash_command(
        name="set-groups-limit",
        description="Returns bot latency."
    )
    @commands.has_permissions(administrator=True)
    async def set_groups_limit(
        self,
        inter: disnake.ApplicationCommandInteraction,
        limit: int
    ):
        async with aiosqlite.connect(settings.DB_PATH) as con:
            await con.execute(
                "UPDATE guilds SET groups_count_limit=? WHERE guild_id=?",
                (limit, inter.guild_id)
            )
            await con.commit()
        await inter.response.send_message(embed=embeds.Success(description="groups_count_limit new value: {0}".format(limit)), ephemeral=True)
    
    @commands.slash_command(
        name="set-groups-enabled",
        description="Returns bot latency."
    )
    @commands.has_permissions(administrator=True)
    async def set_groups_enabled(
        self,
        inter: disnake.ApplicationCommandInteraction,
        enabled: bool
    ):
        async with aiosqlite.connect(settings.DB_PATH) as con:
            await con.execute(
                "UPDATE guilds SET groups_enabled=? WHERE guild_id=?",
                (int(enabled), inter.guild_id)
            )
            await con.commit()
        await inter.response.send_message(embed=embeds.Success(description="groups_enabled new value: {0}".format(enabled)), ephemeral=True)
    
    @commands.slash_command(
        name="del-group-admin",
        description="Returns bot latency."
    )
    @commands.has_permissions(administrator=True)
    async def del_group(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel | None = None
    ):
        # if channel is none, use inter.channel
        if not channel:
            channel = inter.channel
        
        async with aiosqlite.connect(settings.DB_PATH) as con:
            if guild_config := await (await con.execute("SELECT (groups_category_id) FROM guilds WHERE guild_id=?", (inter.guild_id,))).fetchall():
                [groups_category_id] = guild_config[0]
                groups_category = inter.guild.get_channel(groups_category_id)
                if groups_category:
                    if channel in groups_category.text_channels:
                        # send modal window
                        await channel.delete()
                        await inter.response.send_message(embed=embeds.Success(description="Deleted group {0}".format(channel.name)))     
                    else:
                        await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a group.".format(channel.id)))
                else:
                    await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a category".format(groups_category_id)))
            else:
                await inter.response.send_message(embed=embeds.Error(description="Use setup command, before using it."))

    @commands.slash_command(
        name="guild-config"
    )
    @commands.has_permissions(administrator=True)
    async def guild_config(self, inter: disnake.ApplicationCommandInteraction):
        async with aiosqlite.connect(settings.DB_PATH) as con:
            if guild_config := await (await con.execute("SELECT groups_category_id, groups_count_limit, groups_enabled FROM guilds WHERE guild_id=?", (inter.guild_id,))).fetchall():
                embed = embeds.Info(description="Guild configurations:")
                for [key, value] in zip(
                    (
                        "groups_category_id",
                        "groups_count_limit",
                        "groups_enabled"
                    ),
                    guild_config[0]
                ):
                    embed.add_field(f"**{key}**", f"`{value}`", inline=False)
                await inter.response.send_message(embed=embed)
            else:
                await inter.response.send_message(embed=embeds.Error(description="Use setup command, before using it."))            

class AdminVoicesCog(commands.Cog, interfaces.AdminVoicesCommandsInterface):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot

def setup(bot: commands.Bot) -> None:
    bot.add_cog(AdminGroupsCog(bot))
