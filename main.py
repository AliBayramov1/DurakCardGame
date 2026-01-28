import time
import random

card_suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
suits_symbols = {'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'}
card_numbers = ['6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
# for enemy logic maye count the cards of the same suit and find the probability
# of player having the card. If it is lower than 30 % then enemy should make a play. And also
# playing the least valuable cards first

class Game:
    """
    Main logic  of the game

    Contains methods for choosing the first player, displaying the table and starting the game.
    """
    def __init__(self):
        """
        Creates and shuffles the deck, initializes the table, sets the trump card and sets the starting attacker.
        """
        self.deck = [(number, suit) for number in card_numbers for suit in card_suits]  # the initial deck of cards
        random.shuffle(self.deck)  # shuffle the list of cards
        self.current_cards = []  # cards that are currently placed at the table
        self.trump = None  # trump card in the game
        self.player_attack = True

    def who_first(self, *args):  # find which player goes first. Args is a list of Player() objects
        """
        Determines which player goes first

        The person with the lowest trump card starts first

        Parameters:
            *args (Player): Player objects participating in the game

        Returns:
            Player: The Player who goes first
        """
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
        """
        Displays the current table.

        Parameters:
            player (Player): Player participating in the game
            opp (Player): Bot participating in the game
        """
        print('----------------------------------------')
        print(f'Opponent\'s card count: {len(opp.hand)}')
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
        """
        Starts the main game loop.

        Handles role switching, card drawing, win/lose and replay logic.
        """
        # game should go while both players have at least one card in hand and deck is not
        # empty
        input('Press enter to start')

        play = True

        while play:
            player = Player(self, 'Player')
            bot = Player(self, 'Bot')

            self.trump = self.deck[-1][1]
            self.deck[-1], self.deck[0] = self.deck[0], self.deck[-1]  # move the trump card to the bottom of the deck

            if self.who_first(player, bot) == player:
                self.player_attack = True
            else:
                self.player_attack = False

            print('Choose bot difficulty(1.Easy, 2.Hard):')
            difficulty = input()

            while difficulty != '1' and difficulty != '2':
                print('Invalid choice')
                difficulty = input()


            print('Starting the game...')
            print('--------------------------')
            print(f'{self.trump}({suits_symbols[self.trump]}) is the trump card')
            print('--------------------------')
            time.sleep(1)
            if self.player_attack:
                print('You go first')
            else:
                print('Opponent goes first')

            time.sleep(1)

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
                            if not bot.bot_play(player, False, difficulty):
                                for card in self.current_cards:
                                    bot.hand.append(card)
                                self.current_cards.clear()
                                break
                else:
                    while True:
                        if bot.bot_play(player, True, difficulty):
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
    """
    Represents a player in the game

    Player can be a user or a bot and has a hand of cards.

    Contains methods for drawing cards, placing cards and playing cards
    """
    def __init__(self, game, name):
        """
        Defines the game of Player, sets the name of Player, initializers the hand and appends 6 cards to it.

        Parameters:
            game (Game): the game being played
            name (str): the name of Player
        """
        self.game = game
        self.name = name
        self.hand = []

        for i in range(6):  # deal 6 cards to players at the beginning
            rand_num = random.randint(0, len(self.game.deck) - 1)
            self.hand.append(self.game.deck[rand_num])
            del self.game.deck[rand_num]

    def draw_cards(self):  # add cards from the deck to the list of player's cards if the player
        # has less than 6 cards and if the deck is not empty
        """
        Draws the cards from the deck into the hand until the player has 6 cards or the deck is empty.
        """
        if len(self.hand) < 6:
            if len(self.game.deck) > 0:
                count = 0

                while len(self.hand) < 6 and len(self.game.deck) > 0:
                    self.hand.append(self.game.deck.pop())
                    count += 1

                print(f'{self.name} drew {count} cards')
            else:
                print('The deck is empty')
        else:
            print(f'{self.name} has enough cards')


    def place_card(self, card):
        """
        Place the chosen card to the current table.

        Parameters:
            card (tuple): the card to be placed, (number, suit)
        """
        self.game.current_cards.append(card)
        self.hand.remove(card)

    def play_card(self, num, attack):  # check if Player can place a card. If yes, place the card.
        # num is the index of the card in the players hand(because player will be choosing the cards by their index)
        """
        Attempts to play a card from the player's hand.

        Parameters:
            num (int): Index of a chosen card
            attack (bool): True if the player is attacking, False if defending

        Returns:
            bool: True if the card can be placed, False if not
        """
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

    def bot_play(self, p, attack, difficulty):
        """

        Logic for bot's plays.
        If difficulty is set to easy, bot chooses a random card from the set of all valid plays, bot when defending and attacking.

        If difficulty is set to hard, when attacking, bot chooses a card from the list of valid plays that is the least likely
        to be defended by player.
        When defending, bot attempts to use the leat valuable card from the set of all valid plays.

        Parameters:
            p (Player): Player participating in the game
            attack (bool): True if the bot is attacking, False if defending
            difficulty (str): difficulty of hte game. '1' for easy, '2' for hard

        Returns:
            bool: True if the bot plays a card, False if not

        """
        bot_view = self.game.deck + p.hand  # all the possible cards that could potentially be in players hands
        trump = self.game.trump
        if attack:  # when attacking we want to find a list of all the cards that we can place.
            # Then we should find the chances of each card being successfully defended by the player.
            def valid_defense_cards(attack_card): # returns list of all cards that can defend the attack_card
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

            if difficulty == '2':
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

            else:  # difficulty == '1'
                valid_cards = [] # all  the cards bot can play

                for card in self.hand:
                    if any(card[0] == c[0] for c in self.game.current_cards) or len(self.game.current_cards) == 0:
                        valid_cards.append(card)

                if not valid_cards:
                    return False

                self.place_card(random.choice(valid_cards))

                return True


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

            if difficulty == '2':
                non_trump = [x for x in valid_defences if x[1] != trump]

                if non_trump:
                    chosen_card = least_card(non_trump)
                else:
                    chosen_card = least_card(valid_defences)

                self.place_card(chosen_card)

            else:  # difficulty == '1'
                self.place_card(random.choice(valid_defences))

            return True


        # bot logic: sees all the cards left in the deck plus the cards in the players hand.
        # Calculate the chances of a successful play. For example what are the chances of a player
        # successfully defending a card, so a chance that a player does not have a higher number suit
        # or a trump card. We also use the play_card function here.


game = Game()
game.start()
