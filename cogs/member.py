import disnake, datetime
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
            icon_url=disnake.File("icon.png")
        )
        await inter.response.send_message(
            embed=embed,
            ephemeral=True
        )

def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))