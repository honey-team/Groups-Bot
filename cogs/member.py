import disnake, aiosqlite
from aiosqlite import Connection
from disnake.ext import commands
from services.database import *
from services.config import Config
from services.embeds import *
from services.interfaces import MemberCommandsInterface
from services.modals import *

class MemberCog(commands.Cog, MemberCommandsInterface):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.debug = True

    @commands.slash_command(
        name="new-group"
    )
    async def new_group(self, inter: disnake.ApplicationCommandInteraction):
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            guild_config = await Database.Guilds.get_config(db, inter.guild_id)
            groups_category: disnake.CategoryChannel = inter.guild.get_channel(guild_config["groups_category_id"])
            if guild_config["groups_enabled"]:
                # Does category exists
                if groups_category in inter.guild.categories:
                    # Does groups limit
                    if len(groups_category.text_channels) + 1 <= guild_config["groups_limit"]:
                        await inter.response.send_modal(NewGroupModal(groups_category))
                    else:
                        await inter.response.send_message(embed=Error(description="Do not over groups limit"))
                else:
                    await inter.response.send_message(embed=Error(description="Uknown category. Use /set-groups-category"))
            else:
                await inter.response.send_message(embed=Error(description="Groups are not enabled on this guild"))
    
    @commands.slash_command(
        name="edit-group"
    )
    async def edit_group(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel | None = None
    ):
        if not channel:
            channel = inter.channel
        
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            guild_config = await Database.Guilds.get_config(db, inter.guild_id)
            if guild_config["groups_enabled"]:
                old_values = {
                    "name":channel.name,
                    "topic":channel.topic
                }
                groups_category: disnake.CategoryChannel = inter.guild.get_channel(guild_config["groups_category_id"])
                # Does category exists
                if groups_category in inter.guild.categories:
                    # Does channel is a group
                    if channel in groups_category.channels:
                        await inter.response.send_modal(EditGroupModal(channel, old_values))
                    else:
                        await inter.response.send_message(embed=Error(description="<#{0}> is not a group".format(channel.id)))
                else:
                    await inter.response.send_message(embed=Error(description="Uknown category. Use /set-groups-category"))
            else:
                await inter.response.send_message(embed=Error(description="Groups are not enabled on this guild"))
    
    @commands.slash_command(
        name="del-group"
    )
    async def del_group(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel | None = None
    ):
        if not channel:
            channel = inter.channel

        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            guild_config = await Database.Guilds.get_config(db, inter.guild_id)
            if guild_config["groups_enabled"]:
                groups_category: disnake.CategoryChannel = inter.guild.get_channel(guild_config["groups_category_id"])
                if channel.permissions_for(inter.author).manage_permissions:
                    # Does category exists
                    if groups_category in inter.guild.categories:
                        # Does channel is a group
                        if channel in groups_category.channels:
                            await channel.delete()
                            await inter.response.send_message(embed=Success(description="Deleted group {0}".format(channel.name)))
                        else:
                            await inter.response.send_message(embed=Error(description="<#{0}> is not a group".format(channel.id)))
                    else:
                        await inter.response.send_message(embed=Error(description="Uknown category. Use /set-groups-category"))
                else:
                    await inter.response.send_message(embed=Error(description="You have not permissions to do it"))
            else:
                await inter.response.send_message(embed=Error(description="Groups are not enabled on this guild"))

    @commands.slash_command(
        name="hide-group"
    )
    async def hide_group(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel | None = None
    ):
        if not channel:
            channel = inter.channel

        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            guild_config = await Database.Guilds.get_config(db, inter.guild_id)
            if guild_config["groups_enabled"]:
                groups_category: disnake.CategoryChannel = inter.guild.get_channel(guild_config["groups_category_id"])
                # Does category exists
                if groups_category in inter.guild.categories:
                    # Does channel is a group
                    if channel in groups_category.channels:
                        await channel.set_permissions(
                            inter.author,
                            view_channel=False
                        )
                        await inter.response.send_message(embed=Success(description="You hided group {0}".format(channel.name)))
                    else:
                        await inter.response.send_message(embed=Error(description="<#{0}> is not a group".format(channel.id)))
                else:
                    await inter.response.send_message(embed=Error(description="Uknown category. Use /set-groups-category"))
            else:
                await inter.response.send_message(embed=Error(description="Groups are not enabled on this guild"))

    @commands.slash_command(
        name="show-group"
    )
    async def show_group(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel_id: int = commands.Param(None, large=True)
    ):
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            guild_config = await Database.Guilds.get_config(db, inter.guild_id)
            if guild_config["groups_enabled"]:
                groups_category: disnake.CategoryChannel = inter.guild.get_channel(guild_config["groups_category_id"])
                # Does channel exists
                if channel := inter.guild.get_channel(channel_id) or inter.channel:
                    # Does category exists
                    if groups_category in inter.guild.categories:
                        # Does channel is a group
                        if channel in groups_category.channels:
                            await channel.set_permissions(
                                inter.author,
                                view_channel=True
                            )
                            await inter.response.send_message(embed=Success(description="You showed group {0}".format(channel.name)))
                        else:
                            await inter.response.send_message(embed=Error(description="<#{0}> is not a group".format(channel.id)))
                    else:
                        await inter.response.send_message(embed=Error(description="Uknown category. Use /set-groups-category"))
                else:
                    await inter.response.send_message(embed=Error(description="Uknown channel"))
            else:
                await inter.response.send_message(embed=Error(description="Groups are not enabled on this guild"))
    
    @commands.slash_command(
        name="groups-list"
    )
    async def groups_list(
        self,
        inter: disnake.ApplicationCommandInteraction,
        show_id: bool = False
    ):
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            guild_config = await Database.Guilds.get_config(db, inter.guild_id)
            if guild_config["groups_enabled"]:
                groups_category: disnake.CategoryChannel = inter.guild.get_channel(guild_config["groups_category_id"])
                # Does category exists
                if groups_category in inter.guild.categories:
                    # Does groups exists
                    if groups_category.text_channels:
                        embed = Info(description="**Groups list**")
                        # Generate embed
                        for channel in groups_category.text_channels:
                            if show_id:
                                embed.add_field(channel.name, f"{channel.topic} **ID:** {channel.id}", inline=False)
                            else:
                                embed.add_field(channel.name, channel.topic)
                        await inter.response.send_message(embed=embed)
                    else:
                        # Send error
                        await inter.response.send_message(embed=Error(description="No groups have been created"))
                else:
                    await inter.response.send_message(embed=Error(description="Uknown category. Use /set-groups-category"))
            else:
                await inter.response.send_message(embed=Error(description="Groups are not enabled on this guild"))

    @commands.slash_command(
        name="group-info"
    )
    async def group_info(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel | None = None,
        channel_id: int = commands.Param(None, large=True),
        show_id: bool = False
    ):
        # Use channel or channel_id
        channel = channel or inter.guild.get_channel(channel_id)
        # If channel and channel_id None use inter.message.channel
        if not channel:
            channel = inter.channel
        
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            guild_config = await Database.Guilds.get_config(db, inter.guild_id)
            if guild_config["groups_enabled"]:
                groups_category: disnake.CategoryChannel = inter.guild.get_channel(guild_config["groups_category_id"])
                # Does category exists
                if groups_category in inter.guild.categories:
                    # Does channel is a group
                    if channel in groups_category.channels:
                        embed = Info(description="**Group info**")
                        embed.add_field("Name", channel.name)
                        embed.add_field("Description", channel.topic)
                        # Show id if user want
                        if show_id:
                            embed.add_field("ID", channel.id, inline=False)
                        
                        await inter.response.send_message(embed=embed)
                    else:
                        await inter.response.send_message(embed=Error(description="Channel <#{0}> is not a group".format(channel.id)))
                else:
                    await inter.response.send_message(embed=Error(description="Uknown category. Use /set-groups-category"))
            else:
                await inter.response.send_message(embed=Error(description="Groups are not enabled on this guild"))

def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))
