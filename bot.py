import os

from src.core.discord_client import DiscordClient
from discord import Intents
from dotenv import load_dotenv

# Bot intents setup
intents = Intents.default()
intents.typing = False
intents.messages = True
intents.message_content = True

client = DiscordClient(intents=intents)

load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------
# import os
# import sys
# import json
# import logging
# from discord import Intents

# from src.core.logging_formatter import LoggingFormatter
# from src.core.discord_client import DiscordClient


# if not os.path.isfile(f'{os.path.realpath(os.path.dirname(__file__))}/config.json'):
#     sys.exit("'config.json' not found! Please add it and try again.")
# else:
#     with open(f'{os.path.realpath(os.path.dirname(__file__))}/config.json') as file:
#         config = json.load(file)

# # Setup bot intents
# intents = Intents.default()
# intents.typing = False
# intents.messages = True
# intents.message_content = True


# logger = logging.getLogger('discord_bot')
# logger.setLevel(logging.INFO)

# # Console handler
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(LoggingFormatter())

# # File handler
# file_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# file_handler_formatter = logging.Formatter(
#     '[{asctime}] [{levelname:<8}] [{name}] {message}', "%Y-%m-%d %H:%M:%S", style="{"
# )
# file_handler.setFormatter(file_handler_formatter)

# # Add handlers
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)

# client = DiscordClient(intents=intents, logger=logger, config=config)