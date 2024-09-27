import disnake, datetime
from disnake import Localised
from disnake.ext import commands
from services.interfaces import MemberCommandsInterface

class MemberCog(commands.Cog, MemberCommandsInterface):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command(
        name="ping",
        description=MemberCommandsInterface.ping.__doc__
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

def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))