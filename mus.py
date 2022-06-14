"""
Mus
"""
import random

# Constants
VALUES = tuple(range(1, 11))
SUITS = ("oros", "copas", "espadas", "bastos")
NAMES = {1: "as", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
         8: "sota", 9: "caballo", 10: "rey"}
CARDS_PER_HAND = 4
NUM_PLAYERS = 4

class MusGame:
    """
    Class to represent a Mus game
    """
    def __init__(self):
        """
        Initializator
        """        
    
    def __str__(self):
        """
        Human readable representation of the game
        """
        return ""
    
class Card:
    """
    Class to define a single card of the deck
    """
    def __init__(self, value, suit):
        """
        Initialize the card
        """
        self._value = value 
        self._suit = suit
    
    def __str__(self):
        """
        Human readable representation of the card
        """                
        return NAMES[(self._value)] + ' ' + self._suit
    
    def get_value(self):
        return self._value
    
    def get_real_value(self):
        real_value = self._value
        if real_value == 2:
            real_value = 1
        elif real_value == 3:
            real_value = 10
        return real_value
    
class Deck:
    """
    Class to define a whole deck
    """
    
    def __init__(self):
        """
        Initialize the deck
        """        
        self._deck = [Card(value, suit) for suit in SUITS
                      for value in VALUES] 
        self.shuffle()
    
    def __str__(self):
        text = ""
        for card in self._deck:            
            text += card.__str__()
            text += ' '
        return text
    
    def shuffle(self):
        random.shuffle(self._deck)
        
    def deal(self):
        return self._deck.pop(0)
        
class Hand:
    """
    Class to define a hand, made up of 4 cards
    """
    def __init__(self, deck, cards = []):
        """
        Initialize a hand, first 4 cards in the deck
        """
        if cards == []:
            self._cards = [deck.deal() for card in range(CARDS_PER_HAND)]
        else:            
            self._cards = [card for card in cards]
        self.sort()        
        
    def __str__(self):
        text = ""
        for card in self._cards:            
            text += card.__str__()
            text += ' '
        return text
      
    def exchange_cards(self, index1, index2):
        temporary_value = self._cards[index1]._value
        temporary_suit = self._cards[index1]._suit
        self._cards[index1] = Card(self._cards[index2]._value,
                             self._cards[index2]._suit)
        self._cards[index2] = Card(temporary_value, temporary_suit)
    
    def sort(self):
        """
        Sort your hand, bigger cards are set first
        """
        for card1 in range(len(self._cards) - 1):
            for card2 in range(card1 + 1, len(self._cards)):
                if (self._cards[card1].get_real_value() <
                    self._cards[card2].get_real_value()):
                    self.exchange_cards(card1, card2)
    
    def reverse_cards(self):
        """
        Reverse your hand once sorted, smaller cards are set now first
        """
        self.sort()
        self._cards.reverse()
    
    def get_real_values(self):
        """
        Returns the values of your cards ignoring the suit
        """
        return [self._cards[dummy_card].get_real_value()
                for dummy_card in range(len(self._cards))]
    
    def wins_grande(self, hand):        
        counter = 0
        wins = None
        self.sort()
        hand.sort()
        values = self.get_real_values()
        values_other_hand = hand.get_real_values()
        if (values[counter] == values_other_hand[counter]):
            counter += 1
            while (counter < CARDS_PER_HAND and wins == None):
                if (values[counter] == values_other_hand[counter]):
                    counter += 1
                elif (values[counter] < values_other_hand[counter]):
                    wins = False
                else:
                    wins = True
                
        elif (values[counter] < values_other_hand[counter]):
            wins = False
        else:
            wins = True
        print (wins)
        return wins
    
    def wins_pequenya(self, hand):
        counter = 0
        wins = None
        self.sort()
        hand.sort()
        self.reverse_cards()
        hand.reverse_cards()
        values = self.get_real_values()
        values_other_hand = hand.get_real_values()
        if (values[counter] == values_other_hand[counter]):
            counter += 1
            while counter < CARDS_PER_HAND and wins == None:
                if (values[counter] == values_other_hand[counter]):
                    counter += 1
                elif (values[counter] > values_other_hand[counter]):
                    wins = False
                else:
                    wins = True
                
        elif (values[counter] > values_other_hand[counter]):
            wins = False
        else:
            wins = True
        print (wins)
        self.sort()
        hand.sort()
        return wins
    
    def wins_pares(self, hand):
        pass
    def wins_juego(self, hand):
        pass
    def wins_punto(self, hand):
        pass
    
def new_game ():
    deck = Deck()
    hands = [Hand(deck) for player in range(NUM_PLAYERS)]
    for hand in hands:
        print (hand)
    #hands[0].exchange_cards(0, 1)
    #print (hands[0])
    #print ""
    card1 = Card(1, "oros")
    card2 = Card(1, "oros")
    card3 = Card(1, "oros")
    card4 = Card(1, "oros")
    cards = [card1, card2, card3, card4]
    hand1 = Hand(deck, cards)
    hand2 = Hand(deck, cards)
    hand1.wins_grande(hand2)
    hand1.wins_pequenya(hand2)

    for i in range(1, NUM_PLAYERS):
        print ("Contra " + str(i+1))
        print ("Gana grande?")
        print (hands[0].get_real_values())
        print (hands[i].get_real_values())
        hands[0].wins_grande(hands[i])
        print ("Gana pequenya?")
        hands[0].wins_pequenya(hands[i])
        print ("")
    
new_game()
