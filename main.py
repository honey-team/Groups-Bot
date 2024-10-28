# -*- encoding: utf-8 -*-
from disnake.ext import commands
from services import db
import disnake, logging, settings, sys

# init logging
file_log = logging.FileHandler('log.log', "w")
console_out = logging.StreamHandler()

logging.basicConfig(
    handlers=(file_log, console_out), 
    format="[%(asctime)s | %(levelname)s]: %(message)s", 
    datefmt="%m.%d.%Y %H:%M:%S",
    level=logging.INFO
)

# init bot
bot = commands.InteractionBot()
bot.activity = disnake.activity.Streaming(name="groups", url="https://www.google.com")
# bot s events
@bot.event
async def on_ready():
    logging.info("Bot ready")
    await db.create_tables()

bot.load_extensions("cogs")

bot.run(open(settings.TOKEN_FILE_PATH).read())
