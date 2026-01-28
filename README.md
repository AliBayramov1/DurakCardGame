# Durak Card Game (Python)

### A console-based implementation of the Durak card game, written in Python.

## How to Run the Game
Install the game
```bash
git clone https://github.com/AliBayramov1/DurakCardGame.git
cd DurakCardGame
```
Run the game
```bash
python main.py
```
## How it works
- Press Enter to start the game
- Choose the difficulty of the bot you will be playing against
- After that, the trump card and the player who goes first will be revealed
- The main game loop starts

## Game rules
There is a total of 36 cards in the game (4 suits ranging from 6 to Ace). 
At the start of the game, the deck is shuffled and players each get delt 6 cards. 
Suit of the trump card is the suit of the card at the top of the deck.
Player who has the smallest trump card goes first. During the game, players take turns attacking and defending.
The attacking player places cards, while the defending player tries to answer. 
Attacking can only place cards of any number that is already on the board. 
Defending player can defend with cards of the same suit and bigger number or with a trump card. 
After each round players draw cards until they have 6. 
Game ends when one player goes out of cards when the drawing deck is empty. 
That player is the winner.