import time
import random

card_suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
suits_symbols = {'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'}
card_numbers = ['6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
# for enemy logic maye count the cards of the same suit and find the probability
# of player having the card. If it is lower than 30 % then enemy should make a play. And also
# playing the least valuable cards first

class Game:
    def __init__(self):
        self.deck = [(number, suit) for number in card_numbers for suit in card_suits]  # the initial deck of cards
        random.shuffle(self.deck)  # shuffle the list of cards
        self.current_cards = []  # cards that are currently placed at the table
        self.trump = None  # trump card in the game
        self.player_attack = True

    def who_first(self, *args):  # find which player goes first. Args is a list of Player() objects
        least = 'Ace'
        least_player = args[0]
        for player in args:
            for card in player.hand:
                if self.trump in card:
                    if card_numbers.index(card[0]) <= card_numbers.index(least):
                        least = card[0]
                        least_player = player
        return least_player

    def display_table(self, player, opp):
        print('----------------------------------------')
        print(f'Opponents cards')
        for i in range(len(opp.hand)):
            print(f'{i + 1}.({opp.hand[i][0]} {suits_symbols[opp.hand[i][1]]})', end='   ')
        print()
        print('Table:')
        print('[', end='')
        for i in range(len(self.current_cards)):
            if i % 2 == 0:
                print(f'({self.current_cards[i][0]} {suits_symbols[self.current_cards[i][1]]})', end='')
            else:
                print(f' / ({self.current_cards[i][0]} {suits_symbols[self.current_cards[i][1]]})', end='  ')
        print(']')
        print('Your hand:')
        for i in range(len(player.hand)):
            print(f'{i + 1}.({player.hand[i][0]} {suits_symbols[player.hand[i][1]]})', end='   ')
        print()
        print('----------------------------------------')

    def start(self):
        # game should go while both players have at least one card in hand and deck is not
        # empty
        input('Press enter to start')

        play = True

        while play:
            player = Player(self, 'Player')
            bot = Player(self, 'Bot')

            self.trump = self.deck[-1][1]
            if self.who_first(player, bot) == player:
                self.player_attack = True
            else:
                self.player_attack = False


            print('Starting the game...')
            time.sleep(2)
            print('--------------------------')
            print(f'{self.trump}({suits_symbols[self.trump]}) is the trump card')
            print('--------------------------')
            time.sleep(1)
            if self.player_attack:
                print('You go first')
            else:
                print('Opponent goes first')

            time.sleep(1.5)

            while (len(self.deck) > 0) or (len(player.hand) > 0 and len(bot.hand) > 0):  # main game loop
                self.current_cards.clear()
                if self.player_attack:
                    while True:
                        self.display_table(player, bot)

                        print(f'Choose your move(play card 1-{len(player.hand)}, or {len(player.hand) + 1}: stop attacking):')
                        card_choice = input()

                        while not card_choice.isdigit() or card_choice not in [str(x + 1) for x in range(len(player.hand) + 1)]:
                            print('Invalid choice')
                            card_choice = input()

                        if int(card_choice) == len(player.hand) + 1:
                            self.player_attack = not self.player_attack
                            break
                        elif player.play_card(int(card_choice), True):
                            if not bot.bot_play(player, False):
                                for card in self.current_cards:
                                    bot.hand.append(card)
                                self.current_cards.clear()
                                break
                else:
                    while True:
                        if bot.bot_play(player, True):
                            self.display_table(player, bot)

                            print(f'Choose your move(play card 1-{len(player.hand)}, or {len(player.hand) + 1}: take cards):')
                            card_choice = input()

                            while not card_choice.isdigit() or card_choice not in [str(x + 1) for x in range(len(player.hand) + 1)]:
                                print('Invalid choice')
                                card_choice = input()

                            if int(card_choice) == len(player.hand) + 1:
                                for card in self.current_cards:
                                    player.hand.append(card)
                                self.current_cards.clear()
                                break
                            elif player.play_card(int(card_choice), False):
                                continue
                        else:
                            self.player_attack = not self.player_attack
                            self.current_cards.clear()
                            break

                if len(self.deck) > 0:
                    time.sleep(0.5)
                    player.draw_cards()
                    time.sleep(0.5)
                    bot.draw_cards()
                    time.sleep(1)


            if len(player.hand) > 0:
                print('Congratulations!')
            else:
                print('Defeat!')

            print()
            print('Play again?(Yes/No): ')
            choice = input()
            while choice.lower() != 'yes' and choice.lower() != 'no':
                print('Invalid choice')
                choice = input()

            if choice.lower() == 'no':
                play = False


class Player:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.hand = []

        for i in range(6):  # deal 6 cards to players at the beginning
            rand_num = random.randint(0, len(self.game.deck) - 1)
            self.hand.append(self.game.deck[rand_num])
            del self.game.deck[rand_num]

    def draw_cards(self):  # add cards from the deck to the list of player's cards if the player
        # has less than 6 cards and if the deck is not empty
        if len(self.hand) < 6 and len(self.game.deck) > 0:
            print(f'{self.name} drew {6 - len(self.hand)} cards')

            for i in range(6 - len(self.hand)):
                self.hand.append(self.game.deck[i])
                del self.game.deck[i]
        else:
            print(f'{self.name} has enough cards')


    def place_card(self, card):
        self.game.current_cards.append(card)
        self.hand.remove(card)

    def play_card(self, num, attack):  # check if Player can place a card. If yes, place the card.
        # num is the index of the card in the players hand(because player will be choosing the cards by their index)
        if num > len(self.hand):
            return False

        card = self.hand[num - 1]

        if attack:  # player is placing an attacking card
            if len(self.game.current_cards) == 0:
                self.place_card(card)
                return True

            for i in self.game.current_cards:
                if card[0] == i[0]:
                    self.place_card(card)
                    return True
            return False
        else:  # player is defending last placed card
            defend_card = self.game.current_cards[-1]

            if defend_card[1] == self.game.trump and card[1] == self.game.trump:
                if card_numbers.index(card[0]) > card_numbers.index(defend_card[0]):
                    self.place_card(card)
                    return True
                else:
                    return False
            elif defend_card[1] != self.game.trump and card[1] == self.game.trump:
                self.place_card(card)
                return True
            elif defend_card[1] == self.game.trump and card[1] != self.game.trump:
                return False
            else:  # they are both not trump cards
                if card[1] == defend_card[1]:
                    if card_numbers.index(card[0]) > card_numbers.index(defend_card[0]):
                        self.place_card(card)
                        return True
                    else:
                        return False
                else:
                    return False

    def bot_play(self, p, attack):
        bot_view = self.game.deck + p.hand  # all the possible cards that could potentially be in players hands
        trump = self.game.trump
        if attack:  # when attacking we want to find a list of all the cards that we can place.
            # Then we should find the chances of each card being successfully defended by the player.
            def valid_defense_cards(attack_card):
                trump = self.game.trump
                valid = []

                for card in bot_view:
                    if attack_card[1] == trump:
                        if card[1] == trump and card_numbers.index(card[0]) > card_numbers.index(attack_card[0]):
                            valid.append(card)

                    else:
                        if card[1] == trump:
                            valid.append(card)
                        elif card[1] == attack_card[1] and card_numbers.index(card[0]) > card_numbers.index(attack_card[0]):
                            valid.append(card)

                return valid

            chosen = None
            least_defences = 20

            for card in self.hand:
                if any(card[0] == c[0] for c in self.game.current_cards) or len(self.game.current_cards) == 0:  # check if there is a same suit or number
                    possible_defences = len(valid_defense_cards(card))

                    if possible_defences < least_defences:
                        least_defences = possible_defences
                        chosen = card
                    elif possible_defences == least_defences:  # if it's the same we choose less valuable card
                        if card_numbers.index(card[0]) < card_numbers.index(chosen[0]):
                            chosen = card

            if chosen:
                self.place_card(chosen)
                return True

            return False

        else:  # when defending bot will choose the least valuable card. If there is any card available
            # to play other than the trump card, the bot will play that card
            defend_card = self.game.current_cards[-1]
            valid_defences = []  # all the cards that bot can play

            for card in self.hand:
                if defend_card[1] == trump:
                    if card[1] == trump and card_numbers.index(card[0]) > card_numbers.index(defend_card[0]):
                        valid_defences.append(card)
                else:
                    if card[1] == defend_card[1] and card_numbers.index(card[0]) > card_numbers.index(defend_card[0]):
                        valid_defences.append(card)
                    elif card[1] == trump:
                        valid_defences.append(card)

            if not valid_defences:  # bot can't defend the card
                return False

            def least_card(lis):  # find a card with the least number
                least = lis[0]
                for card in lis[1:]:
                    if card_numbers.index(card[0]) < card_numbers.index(least[0]):
                        least = card

                return least

            non_trump = [x for x in valid_defences if x[1] != trump]

            if non_trump:
                chosen_card = least_card(non_trump)
            else:
                chosen_card = least_card(valid_defences)

            self.place_card(chosen_card)

            return True


        # bot logic: sees all the cards left in the deck plus the cards in the players hand.
        # Calculate the chances of a successful play. For example what are the chances of a player
        # successfully defending a card, so a chance that a player does not have a higher number suit
        # or a trump card. We also use the play_card function here.


game = Game()
game.start()
