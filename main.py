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
bot.activity = disnake.activity.Streaming(name="groups", url="https://discord.honey-team.ru")

@bot.event
async def on_ready():
    info("Bot ready")
    await Database.init()

@bot.event
async def on_button_click(inter: disnake.MessageInteraction):
    if inter.component.custom_id == "new-group":
        await bot.cogs["MemberCog"].new_group(inter, ephemeral=True)
    elif inter.component.custom_id == "groups-list":
        await bot.cogs["MemberCog"].groups_list(inter, ephemeral=True)

bot.load_extensions("cogs")

bot.run(Token.get())
