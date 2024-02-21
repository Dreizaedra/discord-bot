import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message: discord.Message):
        if message.content == '/help':
            await message.channel.send(f'{message.author.mention} Here are my available commands:\n'
                                       + '**/help** - Show this message!\n'
                                       + '**/hello** - Say hello!')
        elif message.content == '/hello':
            await message.channel.send(f'Hey {message.author.mention}!')


intents = discord.Intents.default()
intents.typing = False
intents.messages = True
intents.message_content = True
client = CustomClient(intents=intents)


client.run(TOKEN)