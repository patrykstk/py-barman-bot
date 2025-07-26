from dotenv import load_dotenv
import os
from bot import DiscordBot
from utils import log

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

if not DISCORD_BOT_TOKEN:
    log("ERROR", "Environment variable DISCORD_BOT_TOKEN is missing. Please check your .env file.")
    exit(1)

if not GUILD_ID:
    log("WARNING", "GUILD_ID not set. Bot will register global commands.")

my_bot = DiscordBot(DISCORD_BOT_TOKEN, GUILD_ID)
my_bot.run_bot()
