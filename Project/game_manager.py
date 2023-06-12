import random
from os.path import exists

class EquationManager:
    
    _answer:int
    _equation:str

    def generate_answer(self, a, b, char):
        if char == '+':
            return a + b
        return a - b

    def generate_random_equation(self):
        a = random.randint(-100, 700)
        b = random.randint(-100, 700)
        chars = "+-"
        char = random.choice(chars)
        self._answer = self.generate_answer(a, b, char)
        possible_answers = []
        for i in range(2):
            possible_answers.append(random.randint(-800, 1400))
        possible_answers.append(self._answer)
        self._equation = f"{a}{char}{b}="
        return possible_answers
    
    @property
    def answer(self):
        return self._answer
    @property
    def equation(self):
        return self._equation

class Score:
    def __init__(self):
        self._score = 0
        if exists("score.txt"):
            with open("score.txt") as save:
                self._highscore = save.read()
        else: self._highscore = ""

    @property
    def score(self):
        return self._score
    
    @property
    def highscore(self):
        return self._highscore
    
    def add_score(self, amount):
        self._score += amount
    
    def save_score(self):
        if self._score > int(self._highscore or 0):
            file = open("score.txt", "w")
            file.write(str(self._score))
            file.close()