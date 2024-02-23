import discord
from discord.ext import commands
from discord.ext.commands import Context


async def setup(bot) -> None:
    await bot.add_cog(General(bot))


class General(commands.Cog, name="General"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="Help command"
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config['prefix']
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0xBEBEFE
        )
        for cog_name in self.bot.cogs:
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            data = []
            for command in cog_commands:
                description = command.description.partition('\n')[0]
                data.append(f'{prefix}{command.name}: {description}')
            help_text = '\n'.join(data)
            embed.add_field(
                name=i.capitalize(), value=f'```{help_text}```', inline=False
            )
        await context.send(embed=embed)


