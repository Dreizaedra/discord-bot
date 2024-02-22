from random import choice

class HangmanGame():
    def __init__(self, attempt_number: int) -> None:
        self.words = ['PYTHON', 'HANGMAN', 'HELLO', 'HELP', 'DISCORD']
        self.word_to_guess = choice(self.words)
        self.guessed_letters = []
        self.attempts = attempt_number
    
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