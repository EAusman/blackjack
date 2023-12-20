import random
import matplotlib.pyplot as plt

# Create a deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class AIPlayer:
    def __init__(self):
        self.hand = Hand()

    def hit_or_stand(self, dealer_upcard):
        player_value = self.hand.value
        if player_value <= 8:
            return True  # Always hit if total value is 8 or less
        elif player_value >= 17:
            return False  # Always stand if total value is 17 or more
        elif player_value == 9:
            return dealer_upcard in ['2', '3', '4', '5', '6']  # Double down
        elif player_value == 10:
            return dealer_upcard not in ['10', 'A']  # Double down
        elif player_value == 11:
            return True  # Always double down on 11
        elif player_value == 12:
            return dealer_upcard not in ['4', '5', '6']  # Stand
        elif player_value >= 13 and player_value <= 16:
            return dealer_upcard not in ['2', '3', '4', '5', '6']  # Stand
        else:
            return True

class Dealer:
    def __init__(self):
        self.hand = Hand()

    def hit_or_stand(self):
        return self.hand.value < 17

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print("<card hidden>")
    print(dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

def play_game(wins, losses, ties):
    while True:
        deck = Deck()
        deck.shuffle()

        player = AIPlayer()
        dealer = Dealer()

        # Deal two cards to each player
        player.hand.add_card(deck.deal_card())
        player.hand.add_card(deck.deal_card())
        dealer.hand.add_card(deck.deal_card())
        dealer.hand.add_card(deck.deal_card())

        show_some(player.hand, dealer.hand)

        while player.hit_or_stand(dealer.hand.cards[1].rank):
            player.hand.add_card(deck.deal_card())
            player.hand.adjust_for_ace()
            show_some(player.hand, dealer.hand)
            if player.hand.value > 21:
                losses += 1
                print("Player busts! Dealer wins.")
                return wins, losses, ties

        if player.hand.value <= 21:
            while dealer.hit_or_stand():
                dealer.hand.add_card(deck.deal_card())
                dealer.hand.adjust_for_ace()

            show_all(player.hand, dealer.hand)

            if dealer.hand.value > 21:
                wins += 1
                print("Dealer busts! Player wins.")
                return wins, losses, ties
            elif dealer.hand.value > player.hand.value:
                losses += 1
                print("Dealer wins.")
                return wins, losses, ties
            elif dealer.hand.value < player.hand.value:
                wins += 1
                print("Player wins.")
                return wins, losses, ties
            else:
                ties += 1
                print("It's a tie!")
                return wins, losses, ties
            
def plot_results(wins, ties, losses):
    labels = ['Wins', 'Ties', 'Losses']
    values = [wins, ties, losses]

    plt.bar(labels, values, color=['green', 'yellow', 'red'])
    plt.title('Blackjack Game Results')
    plt.xlabel('Outcome')
    plt.ylabel('Frequency')
    plt.show()

wins = 0
losses = 0
ties = 0
num_games = 10000
for i in range(num_games):
    print("\n\n\n\n\n")
    wins, losses, ties = play_game(wins, losses, ties)
print(f"Player wins: {wins}, Ties: {ties}, Losses: {losses}")
plot_results(wins, ties, losses)