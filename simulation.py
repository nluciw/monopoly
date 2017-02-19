import random
import matplotlib.pyplot as plt

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
        
        self.locations.append(self.pos)

    # Perform mechanics of a turn in jail
    def jail_turn(self, d1, d2):
        # leave jail if doubles
        if d1 == d2:
            self.pos += d1+d2
            self.jail = False
            self.jail_try = 0
        # leave jail if third turn in jail
        elif self.jail_try == 2:
            self.pos += d1+d2
            self.jail = False
            self.jail_try = 0
        # iterate turn in jail number
        else:
            self.jail_try += 1             

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
