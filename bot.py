import os
import re
from random import choice
from discord import Client, Message, Intents
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Hangman():
    def __init__(self, attemptNumber: int) -> None:
        self.words = ['PYTHON', 'HANGMAN', 'HELLO', 'HELP', 'DISCORD']
        self.word_to_guess = choice(self.words)
        self.guessed_letters = []
        self.attempts = attemptNumber
    
    def guess_letter(self, letter: str) -> bool:
        if letter in self.guessed_letters or letter not in self.word_to_guess:
            return False # already guessed end of the line
        elif letter in self.word_to_guess:
            self.guessed_letters.append(letter)
            return True # correct guess

    def display_word(self) -> str:
        masked_word = ''
        for letter in self.word_to_guess:
            if letter in self.guessed_letters:
                masked_word += letter
            else:
                masked_word += '\_'
        return masked_word.upper()

class CustomClient(Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message: Message):
        if message.content == '!help':
            await message.channel.send(f'{message.author.mention} Here are my available commands:\n'
                                       + '**!help** - Show this message!\n'
                                       + '**!hello** - Say hello!\n'
                                       + '**!hangman <X>** - Start the Hangman game! X is the number of chances you have to guess the word (6 if empty)')
        elif message.content == '!hello':
            await message.channel.send(f'Hey {message.author.mention}!')
        elif message.content.startswith('!hangman'):
            try:
                if len(message.content.rstrip()) == 8: # 8 is the length of the '!hangman' command
                    attempts_count_prompt = 6
                elif len(re.split(r'\s+', message.content)) == 2:
                    attempts_count_prompt = int(re.split(r'\s+', message.content)[1])
                else:
                    raise
            except:
                await message.channel.send(f'**{message.content}** is not a valid !hangman command.\nType **!help** to see the available commands')
                return
            game = Hangman(attempts_count_prompt)

            await message.channel.send(f'Welcome to the Hangman game {message.author.mention}!\n'
                                       + f'I am thinking of a word with **{len(game.word_to_guess)}** letters:\n'
                                       + f'**{game.display_word()}**\n'
                                       + f'You have **{game.attempts}** attempts to guess the word, Good luck !')
            
            while game.attempts > 0 and '\_' in game.display_word():
                guess = await self.wait_for('message', check=lambda m: m.author == message.author and m.content.isalpha() and len(m.content) == 1, timeout=30.0)
                if not game.guess_letter(guess.content.upper()):
                    game.attempts -= 1
                    await message.channel.send(f'**{guess.content.upper()}** is not in the word or has already been guessed\n' 
                                               + f'You have **{game.attempts}** attempts left')
                else:
                    await message.channel.send(f'**{guess.content.upper()}** is in the word:\n'
                                               + f'**{game.display_word()}**\n'
                                               + f'You have **{game.attempts}** attempts left!')

            await message.channel.send(f'Game Over!\nThe word was **{game.word_to_guess}**')
            

            


intents = Intents.default()
intents.typing = False
intents.messages = True
intents.message_content = True
client = CustomClient(intents=intents)


client.run(TOKEN)