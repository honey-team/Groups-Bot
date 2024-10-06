import disnake, aiosqlite
from logging import *
from disnake.ext import commands
from services.token import Token
from services.config import Config
from services.database import *
from threading import *

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

bot.load_extensions("cogs")

bot.run(Token.get())
