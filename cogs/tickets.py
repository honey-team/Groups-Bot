import disnake, datetime
from disnake.ext import commands
from localization import localised_command, get_command_data
from services.database import Database
import aiosqlite

class TicketCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @localised_command('t_group')
    async def ticket(self, inter):
        pass

    @ticket.sub_command('t_create')
    async def create(self, ctx: disnake.ApplicationCommandInteraction):
        data = get_command_data("t_create", ctx.locale)
        await ctx.response.send_message(data['test'], ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(TicketCog(bot))