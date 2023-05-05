import random #  импортирует библиотеку random для генерации случайных чисел.
import pandas # импортирует библиотеку pandas, которая предоставляет функционал для работы с таблицами и данными в Python.
import matplotlib.pyplot as plt # импортирует подбиблиотеку pyplot из библиотеки matplotlib, которая позволяет строить графики и диаграммы.

MIN_SIZE = 4
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DATA_FILE = 'names.txt'

def read_names(file_name: str) -> list:
    names = []
    with open(file_name, 'r') as file:
        line = file.readline()
        while line:
            names.append('^' + line.replace('\n', '$'))
            line = file.readline()
    return names

class BigramLanguageModel:
    def __init__(self):
        self.count: dict = {}
        self.context: dict = {}
        self.char_number = 0

    def update(self, name: str) -> None:
        bigrams = self.all_bigrams(name)
        self.char_number += len(name) - 2

        for bigram in bigrams:
            if bigram in self.count:
                self.count[bigram] += 1
            else:
                self.count[bigram] = 1

            if bigram[0] in self.context:
                self.context[bigram[0]].append(bigram[1])
            else:
                self.context[bigram[0]] = [bigram[1]]

    def all_bigrams(self, word: str) -> list:
        return [word[i:i+2] for i in range(len(word)-1)]


    def getting_next(self, context: str) -> str:
        variants = self.context[context]
        return random.choice(variants)

    def generate_name(self) -> str:
        word = ''
        next_char = self.getting_next('^')
        while next_char != '$' or len(word) < MIN_SIZE:
            if next_char == '$':
                next_char = self.getting_next(word[-1])
                continue
            word += next_char
            next_char = self.getting_next(word[-1])
        return word[:-1].replace('$', ' ')
        
    def get_probability(self, char: str) -> dict:
        variants = self.context[char]
        data = {}
        for c in variants:
            if c in data:
                data[c] += 1
            else:
                data[c] = 1
        data.pop('$', None)
        return data

    def get_all_probabilities(self) -> dict:
        result = {}
        for char in ALPHABET:
            data = self.get_probability(char)
            for i in ALPHABET:
                if i not in data:
                    data[i] = 0
            result[char] = sorted(list(data.items()), key=lambda x:x[0])
        return result

def create_language_model(data: list) -> BigramLanguageModel:
    model = BigramLanguageModel()
    for name in data:
        model.update(name)
    return model

def table():
    pandas.DataFrame(model.get_all_probabilities())

def graph():
    for i in ALPHABET: 
            data = model.get_probability(i)
            courses = list(data.keys())
            values = list(data.values())
            fig = plt.figure(figsize = (10,5))
            plt.bar(courses, values, color ='black', width = 0.5)

            plt.ylabel("Occurrence in file")
            # plt.title('Probability of characters after char: ')
            plt.title(i)
            plt.show()

data = read_names(DATA_FILE)
model = create_language_model(data)
name = model.generate_name()

while(True):
        print("\n[1] Enter 1 to generate new Name.")
        print("[2] Enter 2 to get all bigram probabilities in table.")
        print("[3] Enter 3 to get bigram probabilities in picture, graph.")
        print("[q] Enter q to quit.")
        select = input('Please enter a value: \n')
        if select == '1':
            # Step 3: Generate a name
            name = model.generate_name()
            print("Generated name:", name)
        elif select == '2':
            # Visualize bigram probabilities with console
            table()
        elif select == '3':
            # Visualize bigram probabilities with picture
            graph()
        elif select == 'q':
            break