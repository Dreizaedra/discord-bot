import re
from discord import Client, Message
from src.cogs.hangman import HangmanGame as Hangman

class DiscordClient(Client):
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