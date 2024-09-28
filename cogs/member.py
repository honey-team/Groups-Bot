import disnake, datetime
from disnake.ext import commands
from services.interfaces import MemberCommandsInterface
from services.modals import *

class MemberCog(commands.Cog, MemberCommandsInterface):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command(
        name="ping"
    )
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Pong!",
            description=f"My ping: **{round(self.bot.latency * 1000)}**",
            color=disnake.Colour.orange(),
            timestamp=datetime.datetime.now(),
        )
        embed.set_footer(
            text="Groups bot",
            icon_url="https://cdn.discordapp.com/attachments/1013814526010982462/1288785943238545418/image.png?ex=66f672f1&is=66f52171&hm=e0db78d214b9aef352a7f80ba42427b79c024abd1c1e1db2bf4bfd8c41aeaed0&"
        )
        await inter.response.send_message(
            embed=embed,
            ephemeral=True
        )
    
    @commands.slash_command(
        name="create_temp_channel"
    )
    async def create_temporary_channel(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_modal(GetTemporaryChannelInfoModal())

    @commands.slash_command(
        name="delete_temp_channel"
    )
    async def delete_temporary_channel(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        permissions = channel.permissions_for(inter.author)
        if permissions.manage_channels:
            await channel.delete()
            # Send response
            embed = disnake.Embed(
                title="Success",
                description="Deleted channel: **{0}**".format(channel.name),
                color=disnake.Colour.green(),
                timestamp=datetime.datetime.now(),
            )
            embed.set_footer(
                text="Groups bot",
                icon_url="https://cdn.discordapp.com/attachments/1013814526010982462/1288785943238545418/image.png?ex=66f672f1&is=66f52171&hm=e0db78d214b9aef352a7f80ba42427b79c024abd1c1e1db2bf4bfd8c41aeaed0&"
            )
            await inter.response.send_message(embed=embed)
        else:
            # Send response
            embed = disnake.Embed(
                title="Error",
                description="You are not channel owner: **{0}**".format(channel.name),
                color=disnake.Colour.red(),
                timestamp=datetime.datetime.now(),
            )
            embed.set_footer(
                text="Groups bot",
                icon_url="https://cdn.discordapp.com/attachments/1013814526010982462/1288785943238545418/image.png?ex=66f672f1&is=66f52171&hm=e0db78d214b9aef352a7f80ba42427b79c024abd1c1e1db2bf4bfd8c41aeaed0&"
            )
            await inter.response.send_message(embed=embed)

    @commands.slash_command(
        name="update_temp_channel"
    )
    async def update_temporary_channel(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        category_id = 1289124625711763466
        # Check, is channel in temporary channels category
        if channel.category_id == category_id:
            # Check, is he an owner of channel 
            permissions = channel.permissions_for(inter.author)
            if permissions.manage_channels:
                # If yes, send a modal
                everyone: disnake.Role = inter.guild.roles[0]
                private = not channel.permissions_for(everyone).read_messages
                await inter.response.send_modal(
                    UpdateTemporaryChannelInfoModal(
                        {
                            "name":channel.name,
                            "description":channel.topic,
                            "private":"1" if private else "0"
                        },
                        channel.id
                    )
                )
            else:
                # Else send an error
                embed = disnake.Embed(
                    title="Error",
                    description="You are not channel owner: **{0}**".format(channel.name),
                    color=disnake.Colour.red(),
                    timestamp=datetime.datetime.now(),
                )
                embed.set_footer(
                    text="Groups bot",
                    icon_url="https://cdn.discordapp.com/attachments/1013814526010982462/1288785943238545418/image.png?ex=66f672f1&is=66f52171&hm=e0db78d214b9aef352a7f80ba42427b79c024abd1c1e1db2bf4bfd8c41aeaed0&"
                )
                await inter.response.send_message(embed=embed)
        else:
            # Else send an error
            embed = disnake.Embed(
                title="Error",
                description="**{0}** is not temporary channel".format(channel.name),
                color=disnake.Colour.red(),
                timestamp=datetime.datetime.now(),
            )
            embed.set_footer(
                text="Groups bot",
                icon_url="https://cdn.discordapp.com/attachments/1013814526010982462/1288785943238545418/image.png?ex=66f672f1&is=66f52171&hm=e0db78d214b9aef352a7f80ba42427b79c024abd1c1e1db2bf4bfd8c41aeaed0&"
            )
            await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))