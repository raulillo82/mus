"""
Mus
"""
import random
import os

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Constants
VALUES = tuple(range(1, 11))
SUITS = ("oros", "copas", "espadas", "bastos")
NAMES = {1: "as", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
         8: "sota", 9: "caballo", 10: "rey"}
#Indexes within the array for each game
GAMES_INDEX = {"Grande": 0, "Pequenya": 1, "Pares": 2, "Juego_punto": 3}
CARDS_PER_HAND = 4
NUM_PLAYERS = 4
NUM_COUPLES = 2
#Mus has 4 games in the same game
GAMES_IN_MUS = 4
NO_PAIRS = 0
PAIR = 1
THREE_OF_A_KIND = 2
DOUBLE_PAIR = 3
POINTS_TO_WIN = 40
#Default amount to bet, also called "envite", this is always 2 as a standard
DEFAULT_BET = 2
#Amount to win when nobody bets
PASS_AMOUNT = 1

#IMAGE
#1040 x 492 pixels
#Modified to 2496 x 1595

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 800
CONTROL_PANEL_WIDTH = 85
TEXT_HOR_MARGIN = 100
TEXT_BORDER_MARGIN = 10
TEXT_SIZE = 20

class MusGame:
    """
    Class to represent a Mus game
    """
    def __init__(self):
        """
        Initializator
        """
        #Scores of both pairs
        self._score_couple_1 = 0
        self._score_couple_2 = 0
        #A deck is needed for the game
        self._deck = Deck()
        #int to know if there's already a winner
        #values: -1 no winner, 0 couple 1, 1 couple 2
        self._winner = -1
        #Mano, player who wins in case of a tie
        self._mano = 0
        #Whose turn it is, at the beginning, it's "mano's" turn
        self._turn = self._mano
        #Amounts bet at each of the games, initialized to 0
        self.reset_bets()
        #Was each of the games played?
        self.reset_game_played()
        #Each player has a hand of 4 cards
        self.hands = [Hand(player, self._deck)
                      for player in range(NUM_PLAYERS)]
        #Status
        #0 After handing out cards (or between games 1 to 4)
        #1 playing grande
        #2 playing pequenya
        #3 playing pairs
        #4 playing juego/punto
        #5 counting points
        self._status = 0
        #Text to be displayed in the middle of the canvas
        self._info_text = ""
        #Text on top right corner displaying who's mano
        self._mano_text = ""
        
        
    def __str__(self):
        """
        Human readable representation of the game
        """
        string = "Player 1 and Player 3: " + str(self.score_couple_1())
        string += '\n'
        string += "Player 2 and Player 4: " + str(self.score_couple_2())
        return string    
       
    def score_couple_1(self):
        return self._score_couple_1
    
    def score_couple_2(self):
        return self._score_couple_2
    
    def set_mano(self, player):
        self._mano = player
        #Also change turn
        self._turn = player
        
    def get_mano(self):
        return self._mano
    
    def set_turn(self, player):
        self._turn = player
        
    def get_turn(self):
        return self._turn
    
    def get_status(self):
        return self._status
    
    def set_status(self, status):
        self._status = status
        
    def get_info_text(self):
        return self._info_text
        
    def set_info_text(self, info_text):
        self._info_text = info_text
        
    def append_info_text(self, info_text):
        self._info_text += info_text

    def get_bet(self, game):
        return self._bets[game]

    def set_bet(self, amount, game):
        #Array index will be the status - 1
        self._bets[game] = amount

    def reset_bets(self):
        self._bets = [0 for bet in range(GAMES_IN_MUS)]

    def get_game_played(self, game):
        return self._game_played[game]

    def toggle_game_played(self, game):
        self._game_played[game] = not(self._game_played[game])

    def reset_game_played(self):
        self._game_played = [False for bet in range(GAMES_IN_MUS)]

    def get_mano_text(self):
        return self._mano_text
    
    def set_mano_text(self, text):
        self._mano_text = text
    
    def winner(self):
        '''
        Method to check if any of the copules
        has reached the score limit to win
        '''
        if self.score_couple_1() >= POINTS_TO_WIN:
            winner_couple = 0
            #print ("Player 1 and Player 3 win!!!")
        elif self.score_couple_2() >= POINTS_TO_WIN:
            winner_couple = 1
            #print ("Player 2 and Player 4 win!!!")
        else:
            winner_couple = -1
        return winner_couple
    
    def increment_score(self, amount, couple):
        '''
        Method to increment the score of a couple
        '''
        if couple == 0:
            self._score_couple_1 += amount
        elif couple == 1:
            self._score_couple_2 += amount
        else:
            print ("Exception in increment score")
           
    def get_partner_id(self, partner):
        '''
        Method to check who's your partner
        '''
        return (partner + 2) % NUM_PLAYERS
    
    def get_hands(self):
        return self.hands

    def manage_bets (self):
        #Show whose turn it is:
        self.set_info_text("Player's " + str(self.get_turn() + 1) + " turn")

        #Show the buttons (bet, pass)
        button2.set_text ("Bet")
        button3.set_text ("Pass")

    def compute_grande(self):
        '''
        Method to play the first of the four games, grande
        '''
        #Logic to check the winner
        winner_grande = 0
        next_player = winner_grande + 1
        for i in range(1, NUM_PLAYERS):        
            if self.hands[winner_grande].wins_grande(self.hands[next_player]) == False:
                winner_grande = next_player        
            next_player += 1
            #print (winner_grande)
        self.set_info_text("Player " + str(winner_grande + 1) + " wins 'Biggest'")
        #If nothing was bet, whoever wins take one point
        if self.get_bet(GAMES_INDEX.get("Grande")) == 0:
            self.set_bet(PASS_AMOUNT, GAMES_INDEX.get("Grande"))
        self.increment_score(self.get_bet(GAMES_INDEX.get("Grande")), winner_grande % 2)
        #print (self)
    
    def compute_pequenya(self):
        '''
        Method to play the 2nd of the four games, pequenya
        '''
        winner_pequenya = 0
        next_player = winner_pequenya + 1
        for i in range(1, NUM_PLAYERS):        
            if self.hands[winner_pequenya].wins_pequenya(self.hands[next_player]) == False:
                winner_pequenya = next_player        
            next_player += 1
            #print (winner_pequenya)
        #Only previous texts with info about Grande have to be kept
        if "Biggest" not in self.get_info_text():
            self.set_info_text ("")
        self.append_info_text("Player " + str(winner_pequenya + 1) + " wins 'Smallest'")
        #If nothing was bet, whoever wins take one point
        if self.get_bet(GAMES_INDEX.get("Pequenya")) == 0:
            self.set_bet(PASS_AMOUNT, GAMES_INDEX.get("Pequenya"))
        self.increment_score(self.get_bet(GAMES_INDEX.get("Pequenya")), winner_pequenya % 2)
        #print (self)
    
    def play_pairs(self):
        '''
        Method to play the 3rd of the four games, pares
        '''
        #Check players with pairs
        players_with_pairs = []
        for i in range(NUM_PLAYERS):
            if self.hands[i].get_pairs() != []:
                players_with_pairs.append(i)
    
        #print (players_with_pairs)
        #If no one has pairs, don't play, display the text
        if (len(players_with_pairs) < 1):# or
            #(len(players_with_pairs) == 2 and
             #players_with_pairs[1] - players_with_pairs[0] != 2)):
            self.append_info_text("Nobody has 'pairs'")
        else:
            #Only play for more than 1 player
            if (len(players_with_pairs) > 1):
                players_with_pairs_iterable = list(players_with_pairs)
                winner_pairs = players_with_pairs.pop(0)
                next_player = players_with_pairs.pop(0)
                for i in range(len(players_with_pairs_iterable) - 1):
                    #print (winner_pairs, next_player)
                    if self.hands[winner_pairs].wins_pares(self.hands[next_player]) == False:
                        winner_pairs = next_player
                    if players_with_pairs != []:
                        next_player = players_with_pairs.pop(0)
                    #print (winner_pairs)
            #If only one player, he wins the pairs
            else:
                winner_pairs = players_with_pairs.pop(0)
            
            self.set_info_text("Player " + str(winner_pairs + 1) + " wins 'Pairs'")
            
            #Count the points according to winner's kind of pairs
            self.increment_score(len(self.hands[winner_pairs].get_pairs()) - 1,
                             winner_pairs % 2)
            #If his couple has pairs, count his points too			           
            if (self.hands[self.get_partner_id(winner_pairs)].get_pairs() != []):
                self.increment_score(
                    len(self.hands[self.get_partner_id(winner_pairs)].get_pairs()) - 1,
                    winner_pairs % 2)
        
        #print (self)
        
    def play_juego_punto (self):
        '''
        Method to play the last of the four games.
        It can be either juego or punto.
        It'll be chosen here
        '''
        #Check who has juego
        players_with_juego = []
        for i in range(NUM_PLAYERS):
            if self.hands[i].has_juego():
                players_with_juego.append(i)
        
        #If nobody, play punto
        if players_with_juego == []:
            self.play_punto()
            
        #Else, play juego
        else:
            self.play_juego()
        
    
    def play_juego(self):
        #print (players_with_juego)
        players_with_juego = []
        for i in range(NUM_PLAYERS):
            if self.hands[i].has_juego():
                players_with_juego.append(i)
                
        #print (players_with_juego)
        
        #This if/else is no longer so useful
        #as we already check this in play_juego_punto
        #It's kind of legacy before that other method was created
        if (len(players_with_juego) < 1):# or
            self.set_info_text("Nobody has 'Game'")
            #(len(players_with_juego) == 2 and
            # players_with_juego[1] - players_with_juego[0] != 2)):
        else:
            #Check who wins if more than 1 player with juego
            if (len(players_with_juego) > 1):
                players_with_juego_iterable = list(players_with_juego)
                winner_juego = players_with_juego.pop(0)
                next_player = players_with_juego.pop(0) 
            
                for i in range(len(players_with_juego_iterable) - 1):
                    #print (winner_pairs, next_player)
                    if self.hands[winner_juego].wins_juego(self.hands[next_player]) == False:
                        winner_juego = next_player
                    if players_with_juego != []:
                        next_player = players_with_juego.pop(0)
                    #print (winner_pairs)
            # Only one player with juego, he wins
            else:
                winner_juego = players_with_juego.pop(0)
           
            self.set_info_text("Player " + str(winner_juego + 1) + " wins 'Game'")
            
            # Check how many points
            if self.hands[winner_juego].get_value_juego() == 31:
                points_winner = 3
            else:
                points_winner = 2
            self.increment_score(points_winner, winner_juego % 2)
            
            # Check if partner has juego and give points
            # accordingly
            juego_partner = self.hands[self.get_partner_id(winner_juego)].get_value_juego()
            if juego_partner > 30:
                if juego_partner == 31:
                    points_partner = 3
                else:
                    points_partner = 2
                self.increment_score(points_partner, winner_juego % 2)
            
        #else:
        #    print ("No se juega el juego")
            
        #print (self)
    
    def play_punto(self):
        winner_punto = 0        
        next_player = winner_punto + 1
        
        #Loop that compares the temporary winner to the
        #next player
        for i in range(1, NUM_PLAYERS):        
            if self.hands[winner_punto].wins_punto(self.hands[next_player]) == False:
                winner_punto = next_player        
            next_player += 1
            #print (winner_grande)
        self.set_info_text("Player " + str(winner_punto + 1) + " wins 'Point'")
        #You just get one point for winning punto
        self.increment_score(1, winner_punto % 2)
        #print (self)
        
    def play(self):
        '''
        Method to play a full game of mus.
        Mostly useful while debugging in the console
        No longer used as game is now focused in the
        graphical interface
        '''
        players = range(NUM_PLAYERS)
        self.set_mano(players[0])
        while self.winner() == -1:  
            print (players)
            #0 Hand out cards and set hand
            self.hands = [Hand(player, self._deck)
                          for player in players]            
            print ("Mano is Player " + str(self.get_mano() + 1))
            #Print hands in the console
            for hand in self.hands:                
                print (hand)
                print (hand.get_real_values())
                
            #1 Play grande
            self.play_grande()
            #2 Play pequenya (if no winner yet)
            if self.winner() == -1:
                self.play_pequenya()
            #3 Play pairs (if no winner yet)
            if self.winner() == -1:
                self.play_pairs()
            #4 Play juego or punto (if no winner yet)
            if self.winner() == -1:
                self.play_juego_punto()
            print ("")
            
            #Change mano
            players.insert(0, players.pop())
            self.set_mano((self.get_mano() + 1) % 4)
            #Get a new deck and shuffle
            self._deck = Deck()
            
        winner = self.winner()
        if winner == 0:
            print ("Player 1 and Player 3 win!!!")
        else:
            print ("Player 2 and Player 4 win!!!")
            
    def play_step(self):
        '''
        Method that plays a full game of mus, step by step.
        Variable status of the Class is used to know in which
        part of the game we are.
        Also variable winner is needed in order not to play if
        there's already a winner.
        '''
        
        if self.winner() == -1:
            #Status 0 -> Deal
            if self.get_status() == 0:
                mano = self.get_mano()
                players = [(NUM_PLAYERS - mano + idx) % NUM_PLAYERS
                           for idx in range(NUM_PLAYERS)]
                #print (players)
                self.hands = [Hand(player, self._deck)
                              for player in players]            
                self.set_mano_text("Starting player is Player " + str(self.get_mano() + 1))        
                self.set_info_text("")
                #Reset bets and the status of each game played
                self.reset_bets()
                self.reset_game_played()
            #Status 1 -> Grande
            #There's no winner check:
            #no one can win between dealing and grande so far
            elif self.get_status() == 1:
                ##Logic to manage the bets
                self.manage_bets()

            #Status 2 -> Pequenya
            elif self.get_status() == 2:
                if self.winner() == -1:
                    ##Logic to manage the bets
                    self.manage_bets()

            #Status 3 -> Pares
            elif self.get_status() == 3:
                if self.winner() == -1:
                    self.play_pairs()
                    
            #Status 4 -> Juego/punto
            elif self.get_status() == 4:
                if self.winner() == -1:
                    self.play_juego_punto()
                #print ("")
                winner = self.winner()
            #Status 5 -> Counting points
            elif self.get_status() == 5:
                if not(self.get_game_played(GAMES_INDEX.get("Grande"))):
                    self.compute_grande()
                #Check that after computing grande, nobody has won yet
                if self.winner() == -1:
                    if not(self.get_game_played(GAMES_INDEX.get("Pequenya"))):
                        self.compute_pequenya()
                #Change mano
                #players.insert(0, players.pop())
                self.set_mano((self.get_mano() + 1) % 4)
                #Get a new deck and shuffle
                self._deck = Deck()
                winner = self.winner()

        #Check for winners
        elif self.winner() == 0:
            self.set_info_text("Player 1 and Player 3 win!!!")
        elif self.winner() == 1:
            self.set_info_text("Player 2 and Player 4 win!!!")
        
        
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
        '''
        Jack is 8, Knight is 9, King is 10
        No real 8, 9, 10 in spanish deck
        '''
        return self._value
    
    def get_suit(self):
        '''
        Only used for graphical representation purposes
        '''
        return self._suit
    
    def get_real_value(self):
        '''
        3s are kings and 2s are 1s (aces) in mus. Map it!
        '''
        real_value = self._value
        if real_value == 2:
            real_value = 1
        elif real_value == 3:
            real_value = 10
        return real_value
    
    def get_value_juego(self):
        '''
        Get value for juego/punto.
        Jacks/Knights/Kings (and 3s) are 10 points worth
        '''
        value_juego = self.get_real_value()
        if value_juego >= 8:
            value_juego = 10
        return value_juego
    
    def get_value_in_image(self):
        '''
        This method is used for the particularities
        of the tiled image that is used in this game
        If there's a new image in a future, it'll need
        to be adjusted
        '''
        value_in_image = self._value
        if value_in_image > 7:
            #We need to skip 8 and 9 in the original tiled image
            value_in_image += 1
        else:
            value_in_image -= 1
        return value_in_image
    
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
        '''
        Method that shuffles the deck
        '''
        random.shuffle(self._deck)
        
    def deal(self):
        '''
        Method to deal a single card from the deck
        '''
        return self._deck.pop(0)
        
class Hand:
    """
    Class to define a hand, made up of 4 cards
    """
    def __init__(self, order, deck = [], cards = []):
        """
        Initialize a hand, first 4 cards in the deck
        """
        if cards == []:
            self._cards = [deck.deal() for card in range(CARDS_PER_HAND)]
        #Use four set cards, for debug purposes
        else:            
            self._cards = [card for card in cards]
        self.sort()
        #Order is the order in which you are (mano)
        #In case of same values for one result,
        #lower order wins.
        #This is known as "mano" (how close you are
        #to mano, in this case)
        self._order = order        
        
    def __str__(self):
        text = ""
        for card in self._cards:            
            text += card.__str__()
            text += ' '
        return text
      
    def exchange_cards(self, index1, index2):
        '''
        Change order in the cars. Used by sort method
        '''
        temporary_value = self._cards[index1]._value
        temporary_suit = self._cards[index1]._suit
        self._cards[index1] = Card(self._cards[index2]._value,
                             self._cards[index2]._suit)
        self._cards[index2] = Card(temporary_value, temporary_suit)
    
    def sort(self):        
        '''
        Sort your hand so that the best cards for grande
        go first. This also sorts your cards for pares &
        juego
        '''
        for card1 in range(len(self._cards) - 1):
            for card2 in range(card1 + 1, len(self._cards)):
                if (self._cards[card1].get_real_value() <
                    self._cards[card2].get_real_value()):
                    self.exchange_cards(card1, card2)
    
    def reverse_cards(self):
        """
        Reverse your hand once sorted,
        smaller cards are set now first.
        Not used any more, as we check pequenya 
        the other way round now (from last card to 1st one)
        """
        self.sort()
        self._cards.reverse()
    
    def get_cards(self):
        return self._cards
        
    def get_order(self):
        """
        Return your order in the game,
        lower order wins in case of tie
        """
        return self._order
    
    def get_real_values(self):
        """
        Returns the values of your cards ignoring the suit
        """
        return [self._cards[dummy_card].get_real_value()
                for dummy_card in range(len(self._cards))]
    
    def get_value_juego(self):
        """
        Returns the value for juego/punto
        """
        value = 0
        #values = self.get_real_values()
        for dummy_card in range(len(self._cards)):
            value += self._cards[dummy_card].get_value_juego()
        
        return value
    
    def wins_grande(self, hand):
        '''
        Checks whether the hand given wins another one
        Returns a boolean
        '''
        counter = 0
        wins = None
        #Sort the cards as a first step
        self.sort()
        hand.sort()
        #Gets the values of each hand
        values = self.get_real_values()
        values_other_hand = hand.get_real_values()
        
        #As card are ordered, you can check cards
        #using indexes (card 0 with card 0, etc)
        #As soon as a value is different, there's a winner
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
        
        #In case of a tie, check "mano" (order)
        if wins == None:
            if self.get_order() < hand.get_order():
                wins = True
            else:
                wins = False
        #print (wins)
        return wins
    
    def wins_pequenya(self, hand):
        '''
        Checks whether the hand given wins another one
        Returns a boolean
        '''
        counter = 3
        wins = None
        #self.sort()
        #hand.sort()
        #self.reverse_cards()
        #hand.reverse_cards()
        #Gets the values of each hand
        values = self.get_real_values()
        values_other_hand = hand.get_real_values()
        
        #As card are ordered, you can check cards
        #using indexes (card 3 with card 3, etc)
        #As soon as a value is different, there's a winner
        #This time, we need to check from end to beginning
        if (values[counter] == values_other_hand[counter]):
            counter -= 1
            while counter >= 0 and wins == None:
                if (values[counter] == values_other_hand[counter]):
                    counter -= 1
                elif (values[counter] > values_other_hand[counter]):
                    wins = False
                else:
                    wins = True                
        elif (values[counter] > values_other_hand[counter]):
            wins = False
        else:
            wins = True        
        #self.sort()
        #hand.sort()
        #In case of a tie, check "mano" (order)
        if wins == None:
            if self.get_order() < hand.get_order():
                wins = True
            else:
                wins = False
        #print (wins)
        return wins
    
    def get_pairs(self):
        '''
        Returns the kind of pairs a hand has.
        Including "NO_PAIRS"
        '''
        #Initialize return value to NO_PAIRS
        kind_of_pairs = NO_PAIRS
        values = self.get_real_values()
        values_to_iterate = list(values)
        pairs_list = []
        #Use another list to iterate, as we want
        #to modify original list
        for card1 in range(len(values_to_iterate) - 1):
            pair_found = False
            for card2 in range(card1 + 1, len(values_to_iterate)):
                if (values_to_iterate[card1] ==
                    values_to_iterate[card2]):
                    pairs_list.append(values[card2])
                    pair_found = True
                    kind_of_pairs += 1
            if pair_found:
                pairs_list.append(values[card1])
            if kind_of_pairs >= THREE_OF_A_KIND:
                #This break is needed in order not to
                #count "medias" and "duples" wrong
                break
        return pairs_list
    
    def wins_pares(self, hand):
        '''
        Checks whether the hand given wins another one
        Returns a boolean
        '''
        wins = None
        own_pairs = self.get_pairs()
        other_pairs = hand.get_pairs()
        #print (own_pairs, other_pairs)
        
        #Don't check if anybody has no pairs
        if len(own_pairs) > 0 and len(other_pairs) > 0:
            #First, check type of pairs
            #If differet, there's a winner
            if len(own_pairs) > len(other_pairs):
                wins = True
            elif len(own_pairs) < len(other_pairs):
                wins = False
            #Else, check between same kind of pairs
            else:
                #For "par" and "medias"
                #Check which is the repeated card
                if len(own_pairs) <= THREE_OF_A_KIND:
                    if own_pairs[0] > other_pairs [0]:
                        wins = True
                    elif own_pairs[0] < other_pairs [0]:
                        wins = False
                #For "duples"
                #winner is the winner of grande
                else:
                    if own_pairs != other_pairs:
                        wins = self.wins_grande(hand)
                
                #If there's still a tie, check mano (order)
                if wins == None:
                    if self.get_order() < hand.get_order():
                        wins = True
                    else:
                        wins = False
        return wins
    
    def has_juego(self):
        '''
        Method that checks if there's "juego"
        '''
        juego = False
        if (self.get_value_juego() >= 31):
            juego = True
        return juego
    
    def wins_juego(self, hand):
        '''
        Checks whether the hand given wins another one
        Returns a boolean
        '''
        wins = None
                       
        #print (juego_own, juego_other)
        juego_own = self.get_value_juego()
        juego_other = hand.get_value_juego()
        
        #Check juego for different values
        # 31 > 32 > 40 > 37 > 36 > 35 > 34
        if juego_own != juego_other:
            if ((juego_own < juego_other and juego_own <= 32) or
                (juego_own > juego_other and juego_own > 32 and
                 juego_other > 32)):                    
                wins = True
            else:
                wins = False
        #If the same value, check "mano" (order)
        else:
            if self.get_order() < hand.get_order():
                wins = True
            else:
                wins = False
                
        
        '''for card_own, card_other in self._cards, hand._cards:
            juego_own += card_own.get_value_juego()
            juego_other += card_other.get_value_juego()
            print (juego_own, juego_other)
        print (juego_own, juego_other)
        '''
        return wins
    
    def wins_punto(self, hand):
        '''
        Checks whether the hand given wins another one
        Returns a boolean
        '''
        
        #Juego al punto
        juego_own = self.get_value_juego()
        juego_other = hand.get_value_juego()
        
        #Just count the values to check who wins
        if juego_own > juego_other:
            wins = True
        elif juego_own < juego_other:
            wins = False
        #If same values, check "mano" (order)
        else:
            if self.get_order() < hand.get_order():
                wins = True
            else:
                wins = False
        return wins
    
def new_game ():
    '''
    Function to play a whole game.
    Commented code allowed to see a full game
    in the console
    '''
    #deck = Deck()
    #hands = [Hand(player, deck) for player in range(NUM_PLAYERS)]
    '''for hand in range(1, NUM_PLAYERS):
        print (hands[0])
        print (hands[hand])
        print (hands[0].wins_juego(hands[hand]))'''
        
    '''for hand in range(1, NUM_PLAYERS):
        print (hands[0])
        print (hands[hand])
        print (hands[0].wins_pares(hands[hand]))'''
    #hands[0].exchange_cards(0, 1)
    #print (hands[0])
    #print ("")
    '''
    card1 = Card(1, "oros")
    card2 = Card(2, "oros")
    card3 = Card(3, "oros")
    card4 = Card(4, "oros")
    card5 = Card(5, "oros")
    card6 = Card(6, "oros")
    cards1 = [card1, card3, card1, card5]
    cards2 = [card1, card3, card1, card6]
    hand1 = Hand(0, deck, cards1)
    hand2 = Hand(1, deck, cards2)    
    hands = [hand1, hand2]
    '''
    
    '''
    for hand in hands:
        print (hand)
        print (hand.get_real_values())
    '''
    
    
    '''
    for i in range(1, NUM_PLAYERS):
    #for i in range(1, len(hands)):
        print (hands[0])
        print ("Contra " + str(i+1))
        print (hands[i])
        
        print ("Gana grande?")
        print (hands[0].get_real_values())
        print (hands[i].get_real_values())
        hands[0].wins_grande(hands[i])
        print ("Gana pequenya?")
        hands[0].wins_pequenya(hands[i])
        print ("Gana pares?")
        print (hands[0].wins_pares(hands[i]))
        print ("Gana juego?")
        print (hands[0].wins_juego(hands[i]))
        
        print ("")
     '''
    partida = MusGame()
    partida.play_step()
    return partida
    
#new_game()
def new_button_handler():
    #Reset button names
    button2.set_text('Next')
    button3.set_text('')
    global game
    game = new_game()    
    
def button2_handler():
    if button2.get_text() == "Next":
        status = game.get_status()
        status += 1
        status %= 6
        game.set_status(status)
        game.play_step()
    elif button2.get_text() == "Bet":
        #Place the bet
        game.set_bet(DEFAULT_BET, game.get_status() - 1)
        #Change turn to next player to call or pass
        game.set_turn((game.get_turn() + 1 ) % NUM_PLAYERS)
        #print(game.get_bet(game.get_status() - 1))
        game.set_info_text(str(game.get_bet(game.get_status() - 1)) + " were bet. Player's " + str(game.get_turn() + 1) + " turn")
        #Change button 2 text to "call"
        button2.set_text("Call")
        #Enable button 3 text to "pass"
        button3.set_text("Pass")
        #Change text to show next player's turn
    elif button2.get_text() == "Call":
        #Bet was closed, will be checked at the end of the game
        #Change turn back to mano
        game.set_turn(game.get_mano())
        #Change buttons text to default
        button2.set_text("Next")
        button3.set_text("")
        #Change text to reset player's turn
        game.set_info_text("Bet was called. Player's " + str(game.get_turn() + 1) + " turn")
    
def button3_handler():
    if button3.get_text() == "Pass":
        #Check whether there was a previous bet
        if game.get_bet(game.get_status() - 1) > 0:
            #There was a bet, "pass" means "reject the bet"
            #Mark game as played. 
            game.toggle_game_played(game.get_status() - 1)
            #Increase score. Whose score? Couple whose turn is not active
            game.increment_score(1, (game.get_turn() + 1) % NUM_COUPLES)
            #Change turn back to mano
            game.set_turn(game.get_mano())
            #Change buttons text to default
            button2.set_text("Next")
            button3.set_text("")
            #Change text to reset player's turn
            game.set_info_text("Player's " + str(game.get_turn() + 1) + " turn")
        #There was no bet rejection, so next player can bet if they want
        elif game.get_bet(game.get_status() - 1) == 0:
            #Change turn to next player
            game.set_turn((game.get_turn() + 1 ) % NUM_PLAYERS)
            #If the turn was already changed 3 times, it's a full round, go to the next game
            if game.get_turn() == game.get_mano():
                #Change buttons text to default
                button2.set_text("Next")
                button3.set_text("")
                #Change text to inform game was not played. Reset player's turn
                #print ((GAMES_INDEX.keys())[0])
                game.set_info_text(list(GAMES_INDEX.keys())[game.get_status() - 1] + " was not played. Player's " + str(game.get_turn() + 1) + " turn")
            #Otherwise, simply switch the turn to the next player
            else:
                #Change text to reset player's turn
                game.set_info_text("Player's " + str(game.get_turn() + 1) + " turn")

def draw_handler(canvas):    
    '''canvas.draw_image(cards_image,
                      #(IMAGE_WIDTH / 2, IMAGE_HEIGHT / 2),
                      #(IMAGE_WIDTH, IMAGE_HEIGHT),
                      (_image_width / 2, _image_height / 2),
                      (_image_width, _image_height),
                      (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2),
                      (CANVAS_WIDTH, CANVAS_HEIGHT))'''
    #Static texts with the names of the players
    canvas.draw_text('Player 1',
                     ((CANVAS_WIDTH - CONTROL_PANEL_WIDTH) / 2,
                      TEXT_BORDER_MARGIN + TEXT_SIZE),
                     TEXT_SIZE, 'Black')
    canvas.draw_text('Player 2',
                     (CANVAS_WIDTH - TEXT_HOR_MARGIN,
                      CANVAS_HEIGHT / 2),
                     TEXT_SIZE, 'Black')
    canvas.draw_text('Player 3',
                     ((CANVAS_WIDTH - CONTROL_PANEL_WIDTH) / 2,
                      CANVAS_HEIGHT - TEXT_SIZE),
                     TEXT_SIZE, 'Black')
    canvas.draw_text('Player 4',
                     (TEXT_BORDER_MARGIN,
                      CANVAS_HEIGHT / 2),
                     TEXT_SIZE, 'Black')
    #Scores
    canvas.draw_text('Player 1 & Player 3: ' + str(game.score_couple_1()),
                     (5, 25), TEXT_SIZE, 'Black')
    canvas.draw_text('Player 2 & Player 4: ' + str(game.score_couple_2()),
                     (5, 50), TEXT_SIZE, 'Black')
    '''canvas.draw_image(cards_image,
                      (card_width * (0.5 + 3),
                       card_height / 2),
                      (card_width, card_height),
                      (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2),
                      (card_width, card_height))''' 
    #Info text in the middle
    canvas.draw_text(game.get_info_text(),
                     (CANVAS_WIDTH / 2 - 200,
                      CANVAS_HEIGHT / 2),
                     TEXT_SIZE, 'Black')
    #"Mano" text on the top right corner
    canvas.draw_text(game.get_mano_text(),
                     (CANVAS_WIDTH - 300,
                      50), TEXT_SIZE, 'Black')
    #Cards of each player
    player = 0
    for hand in game.get_hands():        
        card_pos = [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2]
        incr_vector = (0, 0)
        if player == 0:
            card_pos = [CANVAS_WIDTH / 2 - 1.5 * card_width,
                        TEXT_BORDER_MARGIN + card_height]           
            incr_vector = (card_width, 0)
        elif player == 1:
            card_pos = [CANVAS_WIDTH - TEXT_HOR_MARGIN - card_width,
                        CANVAS_HEIGHT / 2 - 1.5 * card_height]
            incr_vector = (0, card_width)
        elif player == 2:
            card_pos = [CANVAS_WIDTH / 2 - 1.5 * card_width,
                        CANVAS_HEIGHT - TEXT_BORDER_MARGIN - card_height]
            incr_vector = (card_width, 0)
        elif player == 3:
            card_pos = [TEXT_HOR_MARGIN + card_width,
                        CANVAS_HEIGHT / 2 - 1.5 * card_height]
            incr_vector = (0, card_width)
        for card in hand.get_cards():
            x_increment = card.get_value_in_image()
            y_increment = SUITS.index(card.get_suit())
            canvas.draw_image(cards_image,
                              (card_width * (0.5 + x_increment),
                               card_height * (0.5 + y_increment)),
                               (card_width, card_height),
                               card_pos,
                               (card_width, card_height))
            card_pos[0] += incr_vector[0]
            card_pos[1] += incr_vector[1]  
        player += 1
    
'''new_deck = Deck()
new_card = Card(10, "oros")
nueva_mano = Hand(1, new_deck,
                 [new_card, new_card, new_card, new_card])
nueva_mano2 = Hand(0, new_deck,
                  [new_card, new_card, new_card, new_card])

print (nueva_mano.wins_grande(nueva_mano2))'''

#Load the image
cards_image = simplegui.load_image(
    #'https://drive.google.com/file/d/0B9mfaVCj5XQEUWdaanJNeHVpdm8')
    #'https://upload.wikimedia.org/wikipedia/commons/e/e0/Baraja_espa%C3%B1ola_completa.png')
    'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Baraja_espa%C3%B1ola_completa.png/1280px-Baraja_espa%C3%B1ola_completa.png')
    #'https://docs.google.com/uc?export=download&id=0B9mfaVCj5XQEUWdaanJNeHVpdm8')
    #'http://nacho-martin.com/images/posts/naipes.png')
    #'http://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Baraja_espa%C3%B1ola.svg/1280px-Baraja_espa%C3%B1ola.svg.png')
    #'./spanish_deck.jpg')
#Get width and height

#cards_image = simplegui._load_local_image('images/spanish_deck.jpg')

_image_width = cards_image.get_width()
_image_height = cards_image.get_height()

#print (_image_width, _image_height)
#Get card size in the tiled image
card_width = _image_width / (len(NAMES) + 2) #Image has 2 extra cards, 8 and 9, that are not used
card_height = _image_height / (len(SUITS) + 1) #Image has 1 extra row, for the back of the card image
                      
frame = simplegui.create_frame('Mus',
                               CANVAS_WIDTH,
                               CANVAS_HEIGHT,
                               CONTROL_PANEL_WIDTH)
frame.set_canvas_background('Blue')
#Button to start a new game at any point of time
button1 = frame.add_button('New game',
                           new_button_handler)
#This button will be mainly used to go to the next step. However, it can be also used to bet
button2 = frame.add_button('Next',
                           button2_handler)
#This button has no function at the beginning, will show a text to pass when needed
button3 = frame.add_button('',
                           button3_handler)
frame.set_draw_handler(draw_handler)
game = new_game()
frame.start()
#This is a new comment
