import disnake
from rich.console import Console
from disnake.ext import commands
from services.token import get_token

console = Console()
bot = commands.InteractionBot()
bot.activity = disnake.activity.Streaming(name="groups", url="https://www.google.com")

# Handle events

@bot.event
async def on_ready():
    console.log("[white]Bot is running[/]")

bot.load_extensions("cogs")

bot.run(get_token())