from __future__ import annotations
from disnake.ext import commands
from services import db, embeds, modals, interfaces
import aiosqlite, settings, disnake

class MemberGroupsCog(commands.Cog, interfaces.MemberGroupsCommandsInterface):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot
    
    @commands.slash_command(
        name="ping",
        description="Returns bot latency."
    )
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        rounded_ping = round(self.bot.latency * 1000)
        await inter.response.send_message(embeds.Info(description="My ping: **{0}**".format(rounded_ping)))

    @commands.slash_command(
        name="new-group",
        description="Returns bot latency."
    )
    async def new_group(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):
        async with aiosqlite.connect(settings.DB_PATH) as con:
            if guild_config := await (await con.execute("SELECT groups_category_id, groups_count_limit, groups_enabled FROM guilds WHERE guild_id=?", (inter.guild_id,))).fetchall():
                [groups_category_id, groups_count_limit, groups_enabled] = guild_config[0]
                if groups_enabled:
                    if groups_category_id:
                        groups_category = inter.guild.get_channel(groups_category_id)
                        if groups_category:
                            if len(groups_category.text_channels) < groups_count_limit:
                                # send modal window
                                await inter.response.send_modal(modals.NewGroupModal(groups_category=groups_category))
                            else:
                                await inter.response.send_message(embed=embeds.Error(description="You cannot create more than 100 groups".format(groups_count_limit)))
                        else:
                            await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a category".format(groups_category_id)))
                    else:
                        await inter.response.send_message(embed=embeds.Error(description="Use </set-groups-category:1292115205157032052> before using this command.".format(groups_category_id)))
                else:
                    await inter.response.send_message(embed=embeds.Error(description="Groups are not enabled on this guild.".format(groups_category_id)))
            else:
                await inter.response.send_message(embed=embeds.Error(description="Use </setup:1300289012812222497> command, before using it."))

    @commands.slash_command(
        name="edit-group",
        description="Returns bot latency."
    )
    async def edit_group(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel | None = None
    ):
        # if channel is none, use inter.channel
        if not channel:
            channel = inter.channel

        async with aiosqlite.connect(settings.DB_PATH) as con:
            if guild_config := await (await con.execute("SELECT groups_category_id, groups_enabled FROM guilds WHERE guild_id=?", (inter.guild_id,))).fetchall():
                [groups_category_id, groups_enabled] = guild_config[0]
                if groups_enabled:
                    groups_category = inter.guild.get_channel(groups_category_id)
                    if groups_category:
                        if channel in groups_category.text_channels:
                            # send modal window
                            await inter.response.send_modal(modals.EditGroupModal(channel=channel))
                        else:
                            await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a group.".format(channel.id)))
                    else:
                        await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a category".format(groups_category_id)))
                else:
                    await inter.response.send_message(embed=embeds.Error(description="Groups are not enabled on this guild.".format(groups_category_id)))
            else:
                await inter.response.send_message(embed=embeds.Error(description="Use setup command, before using it."))

    @commands.slash_command(
        name="del-group",
        description="Returns bot latency."
    )
    async def del_group(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        # if channel is none, use inter.channel
        if not channel:
            channel = inter.channel
        
        async with aiosqlite.connect(settings.DB_PATH) as con:
            if guild_config := await (await con.execute("SELECT groups_category_id FROM guilds WHERE guild_id=?", (inter.guild_id,))).fetchall():
                [groups_category_id] = guild_config[0]
                groups_category = inter.guild.get_channel(groups_category_id)
                if groups_category:
                    if channel in groups_category.text_channels:
                        # send modal window
                        if channel.permissions_for(inter.author).manage_permissions:
                            await channel.delete()
                            await inter.response.send_message(embed=embeds.Success(description="Deleted group {0}".format(channel.name)))    
                        else:
                            await inter.response.send_message(embed=embeds.Error(description="You are not the channel's owner.".format(channel.id)))    
                    else:
                        await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a group.".format(channel.id)))
                else:
                    await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a category".format(groups_category_id)))
            else:
                await inter.response.send_message(embed=embeds.Error(description="Use setup command, before using it."))

    @commands.slash_command(
        name="groups-list",
        description="Returns bot latency."
    )
    async def groups_list(
        self,
        inter: disnake.ApplicationCommandInteraction,
        show_id: bool = False
    ):
        async with aiosqlite.connect(settings.DB_PATH) as con:
            if guild_config := await (await con.execute("SELECT (groups_category_id) FROM guilds WHERE guild_id=?", (inter.guild_id,))).fetchall():
                [groups_category_id] = guild_config[0]
                groups_category = inter.guild.get_channel(groups_category_id)
                if groups_category:
                    embed = embeds.Info(description="Groups list:")
                    for group in groups_category.text_channels:
                        # if show_id use an id likes a topic
                        embed.add_field(
                            group.name,
                            group.id if show_id else group.topic,
                            inline=False
                        )
                    await inter.response.send_message(embed=embed)
                else:
                    await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a category".format(groups_category_id)))
            else:
                await inter.response.send_message(embed=embeds.Error(description="Use setup command, before using it."))

    @commands.slash_command(
        name="group-info",
        description="Returns bot latency."
    )
    async def group_info(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel,
        show_id: bool = False
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
                        embed = embeds.Info(description="Group info:")
                        embed.add_field(channel.name, channel.id if show_id else channel.topic)
                        await inter.response.send_message(embed=embed)
                    else:
                        await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a group.".format(channel.id)))
                else:
                    await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a category".format(groups_category_id)))
            else:
                await inter.response.send_message(embed=embeds.Error(description="Use setup command, before using it."))
    
    @commands.slash_command(
        name="show-group",
        description="Returns bot latency."
    )
    async def show_group(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel_id: int = commands.Param(None, large=True)
    ):
        channel: disnake.TextChannel = inter.guild.get_channel(channel_id)
        
        if channel:
            async with aiosqlite.connect(settings.DB_PATH) as con:
                if guild_config := await (await con.execute("SELECT (groups_category_id) FROM guilds WHERE guild_id=?", (inter.guild_id,))).fetchall():
                    [groups_category_id] = guild_config[0]
                    groups_category = inter.guild.get_channel(groups_category_id)
                    if groups_category:
                        if channel in groups_category.text_channels:
                            await channel.set_permissions(
                                inter.author,
                                view_channel=True
                            )
                            await inter.response.send_message(embed=embeds.Success(description="You have shown <#{0}>.".format(channel.id)), ephemeral=True)
                        else:
                            await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a group.".format(channel.id)))
                    else:
                        await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a category".format(groups_category_id)))
                else:
                    await inter.response.send_message(embed=embeds.Error(description="Use setup command, before using it."))
        else:
            await inter.response.send_message(embed=embeds.Error(description="Invalid id: {0}".format(channel_id)))
        
    @commands.slash_command(
        name="hide-group",
        description="Returns bot latency."
    )
    async def hide_group(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        async with aiosqlite.connect(settings.DB_PATH) as con:
            if guild_config := await (await con.execute("SELECT (groups_category_id) FROM guilds WHERE guild_id=?", (inter.guild_id,))).fetchall():
                [groups_category_id] = guild_config[0]
                groups_category = inter.guild.get_channel(groups_category_id)
                if groups_category:
                    if channel in groups_category.text_channels:
                        await channel.set_permissions(
                            inter.author,
                            view_channel=False
                        )
                        await inter.response.send_message(embed=embeds.Success(description="You have hidden group."), ephemeral=True)
                    else:
                        await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a group.".format(channel.id)))
                else:
                    await inter.response.send_message(embed=embeds.Error(description="<#{0}> is not a category".format(groups_category_id)))
            else:
                await inter.response.send_message(embed=embeds.Error(description="Use setup command, before using it."))

def setup(bot: commands.Bot) -> None:
    bot.add_cog(MemberGroupsCog(bot))
