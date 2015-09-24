
from os import remove, rename
from datetime import datetime

import solitaire

class Resolver(solitaire.UnknownSolitaire):
    """Класс, проверяющий работу игры.
    Убран весь вывод в консоль.
    Ведется логирование действий для успешных комбинаций.
    Ведется логирование ошибок.
    """
    filename = datetime.now()

    def card_remove(self, card):
        """Переопределение ф-и. Убран вывод на экран"""
        self.on_table[self.card + 1].extend(self.on_table[self.card])
        self.on_table.pop(self.card)
        self.clear_screen()
        result = open('win_{}.txt'.format(self.filename), 'a')
        result.write('card_remove Method {} || {} |moves| {} |card to move| {} \n'\
                .format(self.card, self.on_table[self.card][0], self.moves, self.card_to_move))
        result.close()

    def clear_screen(self):
        """Переопределение ф-и. Убран вывод на экран"""
        pass

    def show_on_table(self):
        """Переопределение ф-и. Убран вывод на экран"""
        pass

    def start_game(self):
        """Переопределение ф-и. Убран вывод на экран. Добавлено логирование"""
        self.rem = False
        self.tries = 3
        self.shuffle_deck()
        self.card_deal(3)
        result = open('win_{}.txt'.format(self.filename), 'a')
        result.write('start_game method {} \n'.format(', '.join(self.shuffled_deck)))
        result.close()

    def next_turn(self):
        """Переопределение ф-и. Убран вывод на экран. Добавлено логирование"""
        def card_index():
            """Подфункция, определяющая индекс карты, которую будем удалять"""
            self.count_possibles()
            for item in self.on_table:
                if self.card in item:
                    if self.card in self.card_to_move:
                        self.card = self.on_table.index(item) - 1
                        break
                elif self.card.isdigit():
                    if self.on_table[int(self.card)-1][0] in self.card_to_move:
                        self.card = int(self.card) - 2
                        break
                else:
                    pass
            return self.card
        try:
            if not self.card.isdigit() and (self.card.lower() == 'next'
                                            or self.card.lower() == 'n'):
                self.card_deal()
                self.clear_screen()
            else:
                card_index()
                self.card_remove(self.card)
        except Exception as err:
            self.clear_screen()
            errors = open('err.txt', 'a')
            errors.write('{0} Error: {1} Try: {2} Card: \
{3} In hand: {4} Cards to remove: {5} Moves: {6}\n\n'\
                .format(datetime.now(), err, self.tries, self.card, \
                self.on_table, self.card_to_move, self.moves))
            errors.close
        result = open('win_{}.txt'.format(self.filename), 'a')
        result.write('next_turnMetod {} \n'.format(self.on_table))
        result.close()
        return self.card

    def is_win(self):
        """Переопределение ф-и. Убран вывод на экран. Добавлено логирование"""
        self.count_possibles()
        def play_again(self):
            """Запуск 2 или третьей попытки"""
            for i in range(len(self.on_table)):
                if isinstance(self.on_table[0], list):
                    self.on_table.extend(self.on_table[0])
                    self.on_table.pop(self.on_table.index(self.on_table[0]))
            self.shuffled_deck = self.on_table[:]
            self.on_table = []
        if self.tries != 0:
            if len(self.on_table) == 2 and len(self.shuffled_deck) == 0:
                result = open('win_{}.txt'.format(self.filename), 'a')
                result.write('{} || Attemt N {} \n\n'.format(', '.join(self.shuffled_deck_copy), str(self.tries)))
                result.close()
#                rename('win_{}.txt'.format(self.filename), 'win_deck_{}.txt'.format(self.filename))
                result = open('win_deck.txt', 'a')
                result.write('{} || {} || Attemt N {} \n\n'.format(datetime.now(), ', '.join(self.shuffled_deck_copy), str(self.tries)))
                result.close()
                self.win = True
            elif len(self.shuffled_deck) == 0 and self.moves == 0:
                self.tries -= 1
                self.clear_screen()
                play_again(self)
                self.card_deal(3)
                self.next_turn()

        else:
            self.win = True
        return self.win


def solver(runs=99):
    """Функция, запускающая тестовый класс"""
    for i in range(runs):
        print('Run:', i)
        new_game = Resolver()
        new_game.start_game()
        new_game.show_on_table()
        while new_game.win != True:
            new_game.is_win()
            if new_game.moves > 0:
                new_game.card = new_game.card_to_move[0]
            else:
                new_game.card = 'n'
            new_game.next_turn()
#            remove('win_{}.txt'.format(new_game.filename))