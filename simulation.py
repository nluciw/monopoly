import random
import matplotlib.pyplot as plt
import numpy as np

""" This script runs the actual simulations for the game. Most of the
    mechanics can be found in the class 'Piece'.

    Define board size and number of turns in script at the end.  
"""

class Piece:
    """ Each instance of this class is a piece in the game. The class
        takes a name and an initial starting point as arguments.
    """

    def __init__(self, name, pos=0):

        self.pos = pos
        self.name = name
        self.locations = []
        self.jail = False
        self.jail_try = 0
        self.jail_free = False

    # Move the piece. Accounts for jail by landing on square 30
    def move(self): 

        # roll the dice
        d1, d2 = self.roll()        

        # check if in jail 
        if self.jail:
            self.jail_turn(d1, d2)
        else:
            self.pos += d1+d2
        # ensure cyclic board
        if self.pos > 39:
            self.pos = self.pos - 40
        # move to jail
        if self.pos == 30:
            self.pos = 10
            self.jail = True
        if self.pos == 7 | self.pos == 22 | self.pos == 36:
            self.draw(chance)
        
        self.locations.append(self.pos)

    # Perform mechanics of a turn in jail
    def jail_turn(self, d1, d2):

        # leave jail if doubles
        if d1 == d2:
            self.pos += d1+d2
            self.jail = False
            self.jail_try = 0
        # get out of jail free card
        elif self.jail_free:
            self.pos += d1+d2
            self.jail = False
            self.jail_try = 0
            self.jail_free = False
        # leave jail if third turn in jail
        elif self.jail_try == 2:
            self.pos += d1+d2
            self.jail = False
            self.jail_try = 0
        # iterate turn in jail number
        else:
            self.jail_try += 1             

    # card draw
    def draw(self, type):

        if type == 'chance':
            card = random.randint(0, 15)

            if card == 0:
                self.pos = 0
            elif card == 1:
                self.pos = 24
            elif card == 2:
                self.pos = 11
            elif card == 3:
                near_util = np.array([12,28])-self.pos
                self.pos += np.min(near_util[near_util>0])                
            elif card == 4:
                near_rail = np.array([5,15,25,35])-self.pos
                self.pos += np.min(near_rail[near_rail>0])
            #elif card == 5:
            elif card == 6:
                self.jail_free = True   
            elif card == 7:
                self.pos -= 3
            elif card == 8:
                self.pos = 10
                self.jail = True
            #elif card == 9:
            #elif card == 10: 
            elif card == 11:
                self.pos = 5
            elif card == 12:
                self.pos = 39
            #elif card == 13:
            #elif card == 14:
            #elif card == 15:           

    # roll two standard dice
    def roll(self):

        min = 1
        max = 6
        d1 = random.randint(min, max)
        d2 = random.randint(min, max)

        return d1, d2        

if __name__ == '__main__':

    # game parameters    
    board_size = 40
    turns = 1000000
    
    # create pieces
    pieces = []
    hat = Piece(name='hat')
    pieces.append(hat)

    # perform turns
    for i in range(turns):
        for piece in pieces:
            piece.move()

    # plot location distribution
    for piece in pieces:
        plt.hist(piece.locations, bins=board_size, range=(0,40))
        plt.title(
            "Distribution of board locations of piece '%s' over %s turns"\
            %(piece.name, str(turns))
            )
        plt.gca().set_xlim(0, 40)
        plt.show()
