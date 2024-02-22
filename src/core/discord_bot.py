import os
from discord import Intents
from discord.ext import commands

class DiscordBot(commands.Bot):
    def __init__(self, intents: Intents, logger, config) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            intents=intents,
            help_command='help',
        )
        self.logger = logger
        self.config = config
