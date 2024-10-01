import disnake
from logging import *
from rich.console import Console
from disnake.ext import commands
from services.token import get_token
from services.database import Database

basicConfig(
    filename="logs.log",
    filemode="w",
    level=INFO
)

bot = commands.InteractionBot()
bot.activity = disnake.activity.Streaming(name="groups", url="https://www.google.com")

@bot.event
async def on_ready():
    info("Bot ready")
    await Database.init()
    print(await Database.test())

bot.load_extensions("cogs")

bot.run(get_token())