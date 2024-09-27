import disnake, datetime
from disnake.ext import commands
from services.interfaces import AdminCommandsInterface

class MemberCog(commands.Cog, AdminCommandsInterface):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))