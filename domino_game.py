#!/usr/bin/env python3
import random


def generate_cards():
    cards = [[i, j] for i in range(0, 7) for j in range(i, 7)]
    return cards


# shuffle the cards to generate the stock (aparentemente se llama asi al pozo del domino)
def shuffle_stock(cards):
    random.shuffle(cards)
    return cards


def take_cards(cards):
    player_one_cards = list(random.sample(cards, 8))
    # cards in the stock after the player one takes 8 cards
    current_stock = [i for i in cards + player_one_cards if i not in cards or i not in player_one_cards]
    player_two_cards = list(random.sample(current_stock, 8))
    # cards in the stock after the player two takes 8 cards
    current_stock = [i for i in current_stock + player_two_cards if
                     i not in current_stock or i not in player_two_cards]
    return [player_one_cards, player_two_cards, current_stock]


def ask_player(player_number):
    player_answer = input('Player ' + str(player_number) + ' Y/N?\n')
    if player_answer == "Y" or player_answer == "y":
        return 1
    elif player_answer == "N" or player_answer == "n":
        return 0
    else:
        print("Must type Y or N")


class DominoGame:
    def __init__(self):
        self.tails = [None, None]
        self.cards = shuffle_stock(generate_cards())
        self.game = take_cards(self.cards)
        self.player_cards = [self.game[0], self.game[1]]
        self.stock = self.game[2]
        self.table_cards = []
        self.start_game()

    def start_game(self):
        self.print_player_cards()
        self.first_domino()
        self.real_game()
        self.get_winner()

    def player_take_from_stock(self, player_number):
        self.player_cards[player_number - 1].append(self.stock.pop())

    def player_throw(self, card, player_number):
        if card in self.player_cards[player_number - 1] and self.compare_tails(card):
            print("Player " + str(player_number) + " throws " + str(card))
            self.assign_tails(card)
            self.player_cards[player_number - 1].remove(card)
            self.table_cards.append(card)
            return True
        elif not self.compare_tails(card):
            print("Can't throw that card\n")
            return False
        else:
            print("Liar!, you don't have " + str(card))
            return False

    def compare_tails(self, card):
        try:
            if self.tails == [None, None] or card[0] == self.tails[0] or card[0] == self.tails[1] or card[1] == \
                    self.tails[0] or card[1] == self.tails[1]:
                return True
            else:
                return False
        except ValueError and IndexError:
            raise ValueError("Can't write that!")

    def assign_tails(self, card):
        try:
            if self.tails == [None, None]:
                self.tails = card[:]
            if card[0] == self.tails[0]:
                self.tails[0] = card[1]
            elif card[0] == self.tails[1]:
                self.tails[1] = card[1]
            elif card[1] == self.tails[0]:
                self.tails[0] = card[0]
            elif card[1] == self.tails[1]:
                self.tails[1] = card[0]
        except ValueError:
            raise ValueError("Cant write that!")

    def first_domino(self):
        i = 6
        while i >= 0:
            print("Does any player have [" + str(i) + "," + str(i) + "]?")

            player_one_answer = ask_player(1)
            # If the player doesn't write y or n
            while player_one_answer != 1 and player_one_answer != 0:
                player_one_answer = ask_player(1)

            if player_one_answer == 1:
                if self.player_throw([i, i], 1):
                    break

            # player doesn't have the card
            if player_one_answer == 0:

                player_two_answer = ask_player(2)
                # If the player doesn't write y or n
                while player_two_answer != 1 and player_two_answer != 0:
                    player_two_answer = ask_player(2)

                if player_two_answer == 1:
                    if self.player_throw([i, i], 2):
                        break
                # player doesn't have the card
                if player_two_answer == 0:
                    i -= 1

    def real_game(self):
        # Real game starts
        print("The syntax to write a cards is for example: 1 1 to write the card [1,1] ")

        # while game is on keep going
        while len(self.stock) > 0 and len(self.player_cards[0]) > 0 and len(self.player_cards[0]) > 0:

            # write table info
            self.write_values()

            player_one_play = input(
                'Player 1 play (write card or take 1 from the stock with S), your cards are: ' + str(
                    self.player_cards[0]) + "\n")
            if player_one_play == "s" or player_one_play == "S":
                try:
                    self.player_take_from_stock(1)
                except IndexError:
                    break
            else:
                try:
                    player_one_play = [int(x) for x in player_one_play.split()]
                    self.player_throw(player_one_play, 1)
                except ValueError:
                    print("Can't write that!")
                    continue

            self.write_values()
            player_two_play = input(
                'Player 2 play (write card or take 1 from the stock with S), your cards are: ' + str(
                    self.player_cards[1]) + "\n")
            if player_two_play == "s" or player_two_play == "S":
                try:
                    self.player_take_from_stock(2)
                except IndexError:
                    break
            else:
                try:
                    player_two_play = [int(x) for x in player_two_play.split()]
                    self.player_throw(player_two_play, 2)
                except ValueError:
                    print("Can't write that!")
                    continue

    def print_player_cards(self):
        print("Player one dominoes:", self.player_cards[0])
        print("Player two dominoes:", self.player_cards[1])

    def write_values(self):
        print("The dominoes on the table are: " + str(self.table_cards))
        print("The left tail is: " + str(self.tails[0]))
        print("The right tail is: " + str(self.tails[1]))

    def get_winner(self):
        if len(self.player_cards[0]) == 0 or len(self.player_cards[0]) < len(self.player_cards[1]):
            print("CONGARTULATIONS PLAYER 1, YOU WON")
        elif len(self.player_cards[1]) == 0 or len(self.player_cards[0]) > len(self.player_cards[1]):
            print("CONGARTULATIONS PLAYER 2, YOU WON")
        else:
            print("YOU BOTH LOSE, IT'S A TIE")


DominoGame()
