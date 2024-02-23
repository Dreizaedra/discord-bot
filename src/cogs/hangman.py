from discord.ext import commands


async def setup(bot) -> None:
    await bot.add_cog(Hangman(bot))


class Hangman(commands.Cog, name="Hangman"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.game_started = False
        self.player = ''

    @commands.hybrid_command(
        name="hangman",
        description="This is a hangman game!",
        # cooldown=10.0
    )
    async def start_game(self, context: commands.Context) -> None:
        if self.player == context.author:
            await context.channel.send('Game ended!')
            self.game_started = False
            self.player = ''
            return
        elif self.game_started:
            await context.channel.send(
                f"Game already started with **{self.player}**\n"
                + f"Please wait until they have finished!"
            )
            return
        self.game_started = True
        self.player = context.author
        await context.channel.send(content=f"Welcome to the Hangman game {self.player.mention}!")




