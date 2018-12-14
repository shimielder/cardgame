"""Это модуль игры-пасьянса.
Правила игры:
Из перемешанной колоды выкладывается по одной карте.
Если какая-то карта оказывается между
двумя одинаковыми мастями или номиналами,
она перекладывается на предыдущую карту.
Пример: [Clubs 8] [Hearts Ace] [Clubs King]
Карта Hearts Ace находится между Clubs,
таким образом, она кладется поверх Clubs 8
Другой пример: [Spades 2] [Diams 2] [Clubs 2]
Карта Diams 2 находится между двойками,
она кладется поверх Spades 2.
Игра ведется до окончания колоды.
Условия победы: на столе должно остаться 2 стопки,
в первой 51 карта, во второй одна.
Если вся колода выложена, но пасьянс не сложился,
карты собираются по порядку начиная с первой карты/стопки карт,
каждая следующая карта/стопка кладется
под низ колоды (если карты рубашкой вниз).
Затем раскладывается по новой.
Всего 3 попытки. Как только попытки будут исчерпаны, игра окончена
"""

from os import system
from datetime import datetime  # для формирования отчета об ошибках

import card


class UnknownSolitaire(card.CardDeck):
    """Класс, наследующий колоду, содержит логику игры"""
    win = False
    moves = 0
    card_to_move = None

    def __init__(self, set_size=52):
        super().__init__(set_size)
        self.tries = 3
        self.card = None

    def start_game(self):
        """Начало игры, по правилам имеется 3 попытки,
        карты мешаются и сразу раздается 3 карты
        """
        self.shuffle_deck()
        self.card_deal(3)

    def clear_screen(self):
        """Очищает экран от старых записей и выводит колоду"""
        try:
            system('clear')
        except Exception:
            system('cls')
        self.show_on_table()

    def next_turn(self):
        """Функция следующего хода."""
        self.card = input('Choose card or number to remove.\
Type Next to next deal. Type Quit to exit game\n')

        def card_index():
            """Подфункция, определяющая индекс карты, которую будем удалять"""
            self.count_possibles()
            for item in self.on_table:
                if self.card in item:
                    if self.card in self.card_to_move:
                        self.card = self.on_table.index(item) - 1
                        break
                elif self.card.isdigit():
                    if self.on_table[int(self.card) - 1][0] in self.card_to_move:
                        self.card = int(self.card) - 2
                        break
                else:
                    print('Card can not be hided')
            return self.card

        try:
            self.card = str(self.card)
            if not self.card.isdigit() and (self.card.lower() == 'next' or
                                            self.card.lower() == 'n'):
                self.is_win()
                self.card_deal()
                self.clear_screen()
            elif not self.card.isdigit() and (self.card.lower() == 'possibles' or
                                              self.card.lower() == 'p'):
                self.clear_screen()
                self.show_possibles()
            elif not self.card.isdigit() and (self.card.lower() == 'sh' or
                                              self.card.lower() == 'show hint'):
                self.clear_screen()
                self.show_possibles()
                print(self.card_to_move)
            elif not self.card.isdigit() and (self.card.lower() == 'quit' or
                                              self.card.lower() == 'q'):
                self.win = True
                self.clear_screen()
            else:
                card_index()
                self.card_remove(self.card)
        except Exception as err:
            self.clear_screen()
            print('Incorrect input: ', err)
            errors = open('errors from solitaire.txt', 'a')  # Логирование перехваченных ошибок

            errors.write('{0} Error: {1} Try: {2} Card: {3} \
            In hand: {4} Cards to remove: {5} Moves: {6}\n\n' \
                         .format(datetime.now(), err, self.tries, self.card, \
                                 self.on_table, self.card_to_move, self.moves))

            errors.close()
        return self.card

    def is_win(self):
        """Функция проверки условия победы"""
        self.count_possibles()

        def play_again(instance):
            for i in range(len(instance.on_table)):
                instance.on_table.extend(instance.on_table[0])
                instance.on_table.pop(instance.on_table.index(instance.on_table[0]))
            instance.shuffled_deck = list(reversed(instance.on_table[:]))
            instance.on_table = []
            return instance.shuffled_deck

        if self.tries != 0:
            if len(self.on_table) == 2 and len(self.shuffled_deck) == 0:
                print('You won!')
                result = open('win_deck.txt', 'a')  # Запись в файл выигрышной комбинации
                result.write('is_win method {} \
                \n'.format(', '.join(self.shuffled_deck_copy)))
                result.close()
                self.win = True
            elif len(self.shuffled_deck) == 0 and self.moves == 0:
                self.tries -= 1
                self.clear_screen()
                play_again(self)
                self.card_deal(3)
                self.next_turn()
                print('You lose this time. {} tries lost'.format(self.tries))
        else:
            print('All attempts has ended!')
            self.win = True
        return self.win

    def card_remove(self, card):
        """Функция, скрывающая карту в колоде"""
        self.on_table[self.card + 1].extend(self.on_table[self.card])
        removed = self.on_table[self.card][0].split(' ')[0] + ' ' + self.on_table[self.card][0].split(' ')[1]
        self.on_table.pop(self.card)
        self.clear_screen()
        print('Card {} hided'.format(removed))

    def count_possibles(self):
        """Считает количество возможных ходов"""
        self.moves = 0
        self.card_to_move = []
        for i in range(len(self.on_table) - 2):
            if (self.on_table[i][0].split(' ')[0]
                    in self.on_table[i + 2][0].split(' ')):
                self.moves += 1
                self.card_to_move.append(self.on_table[i + 1][0])
            elif (self.on_table[i][0].split(' ')[1]
                  in self.on_table[i + 2][0].split(' ')):
                self.moves += 1
                self.card_to_move.append(self.on_table[i + 1][0])
        return self.moves

    def show_possibles(self):
        """Отображает количество возможных ходов,
        но не сами ходы
        """
        self.count_possibles()
        print('There are {} possible moves'.format(self.moves))


def game():
    """Функция, запускающая игру"""
    sol = UnknownSolitaire()
    sol.start_game()
    sol.show_on_table()
    while not sol.win:
        sol.next_turn()
        sol.is_win()


if __name__ == '__main__':
    game()
