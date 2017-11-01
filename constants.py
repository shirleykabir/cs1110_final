# constants.py
# Walker M. White (wmw2)
# November 12, 2014
"""Constants for Breakout

This module global constants for the game Breakout.  These constants 
need to be used in the model, the view, and the controller. As these
are spread across multiple modules, we separate the constants into
their own module. This allows all modules to access them."""
import colormodel
import sys


######### WINDOW CONSTANTS (all coordinates are in pixels) #########

#: the width of the game display 
GAME_WIDTH  = 480
#: the height of the game display
GAME_HEIGHT = 620


######### PADDLE CONSTANTS #########

#: the width of the paddle
PADDLE_WIDTH  = 58
#: the height of the paddle
PADDLE_HEIGHT = 11
#: the distance of the (bottom of the) paddle from the bottom
PADDLE_OFFSET = 30


######### BRICK CONSTANTS #########

#: the horizontal separation between bricks
BRICK_SEP_H    = 5
#: the vertical separation between bricks
BRICK_SEP_V    = 4
#: the height of a brick
BRICK_HEIGHT   = 8
#: the offset of the top brick row from the top
BRICK_Y_OFFSET = 70
#: the number of bricks per row
BRICKS_IN_ROW  = 10
#: the number of rows of bricks, in range 1..10.
BRICK_ROWS     = 10
#: the width of a brick
BRICK_WIDTH    = GAME_WIDTH / BRICKS_IN_ROW - BRICK_SEP_H


######### BALL CONSTANTS #########

#: the diameter of the ball in pixels
BALL_DIAMETER = 18


######### GAME CONSTANTS #########

#: the number of attempts in a game
NUMBER_TURNS = 3
#: state before the game has started
STATE_INACTIVE  = 0
#: state when we are initializing a new game
STATE_NEWGAME   = 1
#: state when we are counting down to the ball serve
STATE_COUNTDOWN = 2
#: state when we are waiting for user to click the mouse
STATE_PAUSED    = 3
#: state when the ball is in play and being animated
STATE_ACTIVE    = 4


######### COMMAND LINE ARGUMENTS TO CHANGE NUMBER OF BRICKS IN ROW #########
"""sys.argv is a list of the command line arguments when you run
python. These arguments are everything after the work python. So
if you start the game typing

    python breakout.py 3 4
    
Python puts ['breakout.py', '3', '4'] into sys.argv. Below, we 
take advantage of this fact to change the constants BRICKS_IN_ROW
and BRICK_ROWS"""

try:
   if (not sys.argv is None and len(sys.argv) == 3):
        bs_in_row  = int(sys.argv[1])
        brick_rows = int(sys.argv[2])
        if (bs_in_row > 0 and brick_rows > 0):
            # ALTER THE CONSTANTS
            BRICKS_IN_ROW  = bs_in_row
            BRICK_ROWS     = brick_rows
            BRICK_WIDTH    = GAME_WIDTH / BRICKS_IN_ROW - BRICK_SEP_H
except: # Leave the contents alone
    pass


######### ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY #########

#BRICK CONSTANT: list of brick colors for different rows
BRICK_COLORS_R = [colormodel.RGB(43,37,34), colormodel.RGB(94,75,55), colormodel.RGB(3,137,158), colormodel.RGB(18,198,222),
                          colormodel.RGB(229,217,177)]
BRICK_COLORS_H = [colormodel.RGB(46,43,16), colormodel.RGB(46,43,16, a=150), colormodel.RGB(176,132,0),
                  colormodel.RGB(230,208,11), colormodel.RGB(217,212,167)]
BRICK_COLORS_S = [colormodel.RGB(3,27,0), colormodel.RGB(9,130,67),
                  colormodel.RGB(112,181,118), colormodel.RGB(165,223,147),
                  colormodel.RGB(220,231,219)]
BRICK_COLORS_G = [colormodel.RGB(242,164,38), colormodel.RGB(239,120,30),
                  colormodel.RGB(192,26,26), colormodel.RGB(122,30,5), 
                  colormodel.RGB(78,43,23)]
#PADDLE CONSTANT: the amount the paddle moves when left or right keys are pressed
AMOUNT_PADDLE_MOVES = 10

#: state when the player has won
STATE_WON = 5
#: state when the player has lost
STATE_LOST = 6
#: state when the game is telling a story
STATE_STORY = 7
#: state where use is asked to start a new game
STATE_PLAYNEWGAME = 8
#: Harry Potter character names to be assigned to player:
# All characters are credted to J.K. Rowling
CHARACTER_NAMES = ["Harry Potter", "Ronald Weasley","Hermione Granger", "Draco Malfoy",
                                                             "Cedric Diggory", "Luna Lovegood",
                                                             "Newt Scamander", "Albus Dumbledore",
                                                             "Tom Riddle", "Neville Longbottom",
                                                             "Bellatrix Lestrange", "Severus Snape", "Gilderoy Lockhart"]
#: If the player wins, the quote corresponding to their house will pop up on the screen:
# All quotes are credited to Harry Potter Wiki and J.K. Rowling.
QUOTES = ["Wit beyond measure is man's greatest treasure!", "Their daring, nerve, and chivalry,\nset Gryffindor apart!", "Those patient Hufflepuffs are\ntrue and unafraid of toil!", "Those cunning Slytherin use any\nmeans to achieve their ends!"]