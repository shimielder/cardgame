"""Это модуль колоды.
На основе заданного значения создает колоду.
Имеет методы, позволяющие перемешать колоду,
раздать любое количество карт,
показать текущую перемешанную колоду,
показать карты на столе/в руке.
"""
from random import randint
import sys

class CardDeck:

    """ Базовый класс карточной колоды.
    На входе принимает значения 52 или 36 (размер колоды).
    По умолчанию используется 52.
    """

    def __init__(self, set_size=52):
        """На основании заданного размера колоды формирует саму колоду"""
        suits = ('Clubs', 'Diams', 'Hearts', 'Spades')
        self.deck = []
        self.on_table = []
        self.shuffled_deck=[]
        self.shuffled_deck_copy=[]
        if set_size == 52:
            ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
            for suit in suits:
                for rank in ranks:
                    self.deck.append(suit + ' ' + rank)

        elif set_size == 36:
            ranks = ('6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
            for suit in suits:
                for rank in ranks:
                    self.deck.append(suit + ' ' + rank)
        else:
            print('Size should be 52 or 36!')
            sys.exit()


    def display_deck(self):
        """Выводит в консоль сформированную колоду"""
        for item in self.deck:
            print(item)

    def shuffle_deck(self):
        """Перемешивает колоду в случайном порядке.
        Краткое описание алгоритма:
        Исходная колода представлена в виде списока.
        Все манипуляции производятся над копией колоды.
        Берется последний элемент (n) и меняется местами с рандомным элементом в диапазоне (0,n).
        Затем n уменьшается на один и так далее.
        """
        self.shuffled_deck = self.deck[:]
        length = len(self.shuffled_deck)
        while length != 0:
            rand_number = randint(0, length-1)
            self.shuffled_deck[length-1], self.shuffled_deck[rand_number] = self.shuffled_deck[rand_number], \
                                                        self.shuffled_deck[length - 1]
            length -= 1
        self.shuffled_deck_copy = self.shuffled_deck[:]


    def show_shuffled(self):
        """Отображает в консоли перемешанную колоду"""
        try:
            for item in self.shuffled_deck:
                print(item)
        except AttributeError:
            print('Deck isn\'t shuffled yet') #Если колоды нет, выдает ошибку

    def show_on_table(self):
        """Отображает карты, выложенные на стол"""
        for j, k in list(enumerate(self.on_table)):
            print('{}\t[{}\t{}]'.format(j + 1, k[0].split(' ')[0], k[0].split(' ')[1]))


    def card_deal(self, deal=1):
        """Выкладывает на стол указанное количество карт
        По умолчанию, одна карта, но при вызове можно указать любое количество
        """
        while deal != 0:
            self.on_table.append([self.shuffled_deck[len(self.shuffled_deck) - 1]])
            self.shuffled_deck.pop()
            deal -= 1
        return self.on_table[len(self.on_table)-1]
