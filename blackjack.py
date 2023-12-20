import random

#Set up the deck
card_categories = ['Hearts','Diamonds','Clubs','Spades']
cards_list = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
deck = [(card,category) for category in card_categories for card in cards_list]

#returns card value given card
def card_value(card):
    if card[0] in ['Jack','Queen','King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])


#Shuffle and deal
random.shuffle(deck)
player_card = [deck.pop(),deck.pop()]
dealer_card = [deck.pop(),deck.pop()]

#simulate move here (for now implement human choices)
def make_move():
   return input("1 to play, 2 to stop\n")

reward = 0
#play the game
while True:
    player_score = sum(card_value(card) for card in player_card)
    dealer_score = sum(card_value(card) for card in dealer_card)
    print("Cards Player Has:", player_card)
    print("Score Of The Player:", player_score)
    choice = make_move()
    if choice == '1':
        new_card = deck.pop()
        player_card.append(new_card)
    elif choice == '2':
        break
    else:
        print("invalid choice try again")
        continue
    if player_score > 21:
        reward -=3
        break
while dealer_score < 17:
    new_card = deck.pop()
    dealer_card.append(new_card)
    dealer_score+=card_value(new_card)
if dealer_score > 21:
    reward +=1
elif player_score > dealer_score:
    reward+=1
elif dealer_score > player_score:
    reward-=2
else:
    reward -=1

print("reward: "+ str(reward))
