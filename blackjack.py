# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
new_deck = []
player_hand = []
dealer_hand = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hands = []    	

    def __str__(self):
        # return a string representation of a hand, use indexes
        blank = ""
        for i in range(len(self.hands)):
            blank += str(self.hands[i]) + " "
        return "Hands contain " + blank
        
    def add_card(self, card):
        # add a card object to a hand
        self.hands.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        for i in self.hands:
            hand_value += VALUES.get(i.get_rank())    
        for i in self.hands:
            if i.get_rank() != "A":
                return hand_value
            else:
                if hand_value + 10 <= 21:
                    return hand_value + 10
                else:
                    return hand_value
        return hand_value
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        x = 73
        for i in self.hands:
            i.draw(canvas, [pos[0] + x, pos[1]])
            x += 100
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.decks = []
        for suit in SUITS:
            for rank in RANKS:
                self.decks.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.decks)

    def deal_card(self):
        # deal a card object from the deck
        return self.decks.pop()
    
    def __str__(self):
        # return a string representing the deck
        blank = ""
        for i in range(len(self.decks)):
            blank += str(self.decks[i]) + " "
        return "Deck contains " + blank



#define event handlers for buttons
def deal():
    global outcome, in_play, new_deck, player_hand, dealer_hand, score
    #create deck, player's hand, dealer's hand
#    in_play = True
    if in_play == True:
        score -= 1
    new_deck = Deck()
    new_deck.shuffle()
    outcome = "New Game!"
            
    player_hand = Hand()
    player_hand.add_card(new_deck.deal_card())
    player_hand.add_card(new_deck.deal_card())
    print "Player:", player_hand
        
    dealer_hand = Hand()
    dealer_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())
    print "Dealer:", dealer_hand
    in_play = True

def hit():
    global new_deck, player_hand, dealer_hand, in_play, outcome, score
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() <= 21 and in_play == True:
        player_hand.add_card(new_deck.deal_card())
        outcome = "Hit or Stand?"
        print "Player:", player_hand
        print "Dealer:", dealer_hand
    if player_hand.get_value() > 21 and in_play == True:
        outcome = "You have busted!"
        score -= 1
        in_play = False
        print "Player:", player_hand
        print "Dealer:", dealer_hand

def stand():
    global new_deck, player_hand, dealer_hand, in_play, outcome, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if player_hand.get_value() > 21 and in_play == True:
        outcome = "Player has already busted"
        score -= 1
        in_play = False
    else:
        while dealer_hand.get_value() <= 17 and in_play == True:
            dealer_hand.add_card(new_deck.deal_card())
            outcome = "Dealer's Hand"
    if dealer_hand.get_value() > 21 and player_hand.get_value() <= 21 and in_play == True:
        outcome = "Dealer has busted"
        score += 1
        in_play = False
#    elif dealer_hand.get_value() <= 21 and player_hand.get_value() > 21 and in_play == True:
#        outcome = "Player has busted"
#        score -= 1
#        in_play = False
    elif player_hand.get_value() > dealer_hand.get_value() and in_play == True:
        outcome = "Player has won!"
        score += 1
        print "Player:", player_hand
        print "Dealer:", dealer_hand
        in_play = False
    elif player_hand.get_value() <= dealer_hand.get_value() and in_play == True:
        outcome = "Dealer has won!"
        score -= 1
        print "Player:", player_hand
        print "Dealer:", dealer_hand
        in_play = False
    # assign a message to outcome, update in_play and score
    

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, dealer_hand, outcome
    if in_play == True:
        player_hand.draw(canvas, [40, 400])
        dealer_hand.draw(canvas, [40, 170])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,[149, 220], CARD_BACK_SIZE)
    elif in_play == False:
        player_hand.draw(canvas, [40, 400])
        dealer_hand.draw(canvas, [40, 170])        
    canvas.draw_text("Dealer", [110, 150], 50, "Purple")
    canvas.draw_text("Player", [110, 380], 50, "Blue")
    canvas.draw_text(outcome, [300, 380], 35, "Orange")
    canvas.draw_text(str(score), [400, 150], 50, "Orange")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric