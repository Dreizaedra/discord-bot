import os
import sys
import json
import logging
from discord import Intents
from dotenv import load_dotenv

from src.core.logging_formatter import LoggingFormatter
from src.core.discord_bot import DiscordBot


if not os.path.isfile(f'{os.path.realpath(os.path.dirname(__file__))}/config.json'):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f'{os.path.realpath(os.path.dirname(__file__))}/config.json') as file:
        config = json.load(file)

# Setup bot intents
intents = Intents.default()
intents.typing = False
intents.messages = True
intents.message_content = True


logger = logging.getLogger('discord_bot')
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

# File handler
file_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
file_handler_formatter = logging.Formatter(
    '[{asctime}] [{levelname:<8}] [{name}] {message}', "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

load_dotenv()
bot = DiscordBot(intents=intents, logger=logger, config=config)
bot.run(os.getenv('DISCORD_TOKEN'))
