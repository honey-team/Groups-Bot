import disnake
from disnake.ext import commands
from services.token import get_token

bot = commands.Bot(command_prefix=None)
bot.activity = disnake.activity.Streaming(name="groups", url="https://www.google.com")

@bot.event
async def on_ready():
    print("Bot ready")

bot.load_extension("cogs.member")

bot.run(get_token())