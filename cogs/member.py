import json
import disnake, datetime, aiosqlite
from disnake import Localised
from disnake.ext import commands
from services.embeds import *
from services.config import Config
from services.database import Database
from services.interfaces import MemberCommandsInterface
from services.modals import GetTemporaryChannelInfoModal, EditTemporaryChannelInfoModal
from localization import localised_command, get_command_data

class MemberCog(commands.Cog, MemberCommandsInterface):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.debug = True
    
    @localised_command()
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        data = get_command_data("ping", inter.locale)
        embed = disnake.Embed(
            title=data['SUCCESS'], 
            description=data['answer'].format(ping=round(self.bot.latency * 1000)),
            color=disnake.Colour.orange(),
            timestamp=datetime.datetime.now(),
        )
        await inter.response.send_message(
            embed=embed,
            ephemeral=True
        )
    
    @commands.slash_command(
        name="new-group"
    )
    async def create_temporary_channel(self, inter: disnake.ApplicationCommandInteraction):
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            if user_config := await Database.Users.get_config(db, inter.author.id):
                if guild_config := await Database.Guilds.get_config(db, inter.guild_id):
                    if user_config["temp_channels_count"] < guild_config["text_channels_user_limit"]:
                        if temp_channels_count := await Database.TempChannels.count(db, inter.guild_id):
                            if temp_channels_count + 1 < guild_config["text_channels_limit"]:
                                await inter.response.send_modal(GetTemporaryChannelInfoModal())
                            else:
                                await inter.response.send_message(embed=Error(description="You are over the guild temporary channels limit"))
                        else:
                            await inter.response.send_message(embed=Error(description="There is no temporary channels on this guild"))
                    else:
                        await inter.response.send_message(embed=Error(description="You are over the user temporary channels limit"))
                else:
                    await inter.response.send_message(embed=Error(description="There is no temporary channels on this guild"))
            else:
                await db.execute("INSERT INTO users VALUES (?, ?, ?)",
                    (
                        inter.author.id, # user_id
                        0, # temp_channels_count
                        "0" # last_temp_channel_created
                    )
                )
                await db.commit()
                await inter.response.send_message(embed=Info(description="Call that command again."))

    
    @commands.slash_command(
        name="edit-group"
    )
    async def update_temporary_channel(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        await inter.response.send_modal(EditTemporaryChannelInfoModal(channel))
    
    @commands.slash_command(
        name="delete-group"
    )
    async def delete_temporary_channel(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        DB_PATH = Config["paths"]["database"]
        
        async with aiosqlite.connect(DB_PATH) as db:
            if group_config := await Database.TempChannels.get_config(db, channel.id):
                if inter.author.id in group_config["owners"]:
                    await channel.delete()
                    await inter.response.send_message(embed=Success(description="Removed <#{0}>".format(channel.id)))
                else:
                    await inter.response.send_message(embed=Error(description="You must be an owner of <#{0}>".format(channel.id)))
            else:
                await inter.response.send_message(embed=Error(description="<#{0}> is not a group".format(channel.id)))

def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))