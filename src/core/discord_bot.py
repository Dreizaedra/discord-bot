import os
import platform
import random

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context


class DiscordBot(commands.Bot):
    def __init__(self, intents: discord.Intents, logger, config) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(config['prefix']),
            intents=intents,
            help_command=None,
        )
        self.logger = logger
        self.config = config

    async def load_cogs(self) -> None:
        for file in os.listdir(f'{os.path.realpath(os.path.dirname(__file__))}/../cogs'):
            if file.endswith('.py'):
                extension = file[:-3]
                try:
                    await self.load_extension(f'cogs.{extension}')
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f'{type(e).__name__}: {e}'
                    self.logger.error(
                        f'Failed to load extension {extension}\n{exception}'
                    )

    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        statuses = ['With you!', 'With me!', 'With hoomans!']
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        self.logger.info(f'Logged in as {self.user.name}')
        self.logger.info(f'discord.py API version: {discord.__version__}')
        self.logger.info(f'Python version: {platform.python_version()}')
        self.logger.info(
            f'Running on {platform.system()} {platform.release()} {os.name}'
        )
        self.logger.info(f'--------------------------------')

        await self.load_cogs()
        self.status_task.start()

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        full_command_name = context.command.qualified_name
        split = full_command_name.split(' ')
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f'Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) '
                + f'by {context.author} (ID: {context.author.id})'
            )
        else:
            self.logger.info(
                f'Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs'
            )

    async def on_command_error(self, context: Context, error) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description='You are not the owner of this bot!', color=0xE02B2B
            )
            await context.send(embed=embed)
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild "
                    + f"{context.guild.name} (ID: {context.guild.id}), but the user is not an owner of this bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id} tried to execute an owner only command in the bot's "
                    + f"DMs, but the user is not an owner of this bot"
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                            + ", ".join(error.missing_permissions)
                            + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                            + ", ".join(error.missing_permissions)
                            + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error
