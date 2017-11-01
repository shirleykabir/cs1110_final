# play.py
# Sneha Kumar (sk2279), Shirley Kabir(szk4)
# December 7th, 2016
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *
import random

# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
        _playerLives    [boolean]: True as long as the ball does not hit the bottom
                        wall
        
        _playerName     [str]
                        String randomly assigned from a list of characters
                        mentioned in the Harry Potter novels
        
        _playerHouse    [str]: The Hogwart house of the player that is determined by the
                        _playerName
        
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBricks(self):
        """Returns: the list of Brick objects of the game.
        
        This getter method is to protect access to the bricks.
        """
        
        return self._bricks
    
    def getPaddle(self):
        """Returns: the Paddle object of the game.
        
        This getter method is to protect access to the paddle.
        """
        
        return self._paddle
    
    def getBall(self):
        """Returns: the Ball object of the game.
        
        This getter method is to protect access to the ball.
        """
        
        return self._ball
    
    def getPlayerLives(self):
        """Returns: the boolean that determines if the player has lost a life.
        
        This getter method is to protect access to the _playerLives.
        """
        
        return self._playerLives   
    
    def getPlayerHouse(self):
        """Returns: the house of the player.
        
        This getter method is to protect access to the player's Hogwart's House
        """
        
        return self._playerHouse
    
    def getPlayerName(self):
        """Returns: the name of the player
        
        This getter method is to protect access to the player's name
        """
        
        return self._playerName
    
    def setPlayerName(self, name):
        """This method sets the player's name to the value provided.
        
        Parameter name: the name to set the _playerName attribute to
        Precondition: name is a nonempty string that is in the CHARACTER_NAMES constant list.
        """
        
        assert isinstance(name, str), "name is not an instance of String"
        assert name in CHARACTER_NAMES, "name is not from the CHARACTER_NAMES list"
        self._playerName = name
        
    def setPlayerHouse(self,house):
        """This sets the player's house to the value provided
        Parameter house: the Hogwart's house that the player is in
        Precondition: house is a nonempty string that has a valid house name
        """
        
        assert isinstance(house, str), "house is not an instance of String"
        self._playerHouse = house
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializer: Creates an instance of Play.
        
        A play object sets the player's name at random, determines and sets the
        player's house, creates the bricks and paddle for the game and sets the
        default value of if the player is alive to True.
        """
        
        self.setPlayerName(random.choice(CHARACTER_NAMES))
        self.determineHouse()
        self.makeBricks()
        self._paddle = Paddle(x = GAME_WIDTH/2, y=PADDLE_OFFSET, width=PADDLE_WIDTH,
                              height=PADDLE_HEIGHT, linecolor=colormodel.BLACK,
                              fillcolor=colormodel.RGB(130, 82, 1))
        self._playerLives = True
        
    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    
    #Used arrow.py from class to create this method
    def updatePaddle(self, i):
        """This method changes the direction that the paddle moves and how
        far by the keyboard interaction with the user and allows for the paddle
        to move along with the user's use of left and right arrows.
        
        Parameter input: The user input.
        Precondition: input is an instance of the GInput object
        """
        assert isinstance(i, GInput), "i is not a valid GInput"
        
        # Used some of Professor White's lecture code.
        
        if i.is_key_down('left') and self.getPaddle().left >= AMOUNT_PADDLE_MOVES:
            self.getPaddle().x -= AMOUNT_PADDLE_MOVES
        if i.is_key_down('right') and self.getPaddle().right <= GAME_WIDTH-AMOUNT_PADDLE_MOVES:
            self.getPaddle().x += AMOUNT_PADDLE_MOVES
            
    def updateBall(self):
        """Updates the ball so that it bounces when it hits a wall, the paddle,
        or any of the bricks that are still on the screen and removes the brick that has collided with the ball.
        """
        
        self.getBall().moveBall()
        self.getPaddle().moveAfterPaddle(self.getBall())
        
        for brick in self.getBricks():
            if(brick.collidesWithBrick(self.getBall())):
                brick.moveAfterBrick(self.getBall())
                self.getBricks().remove(brick)
            
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self, view):
        """Draws the bricks that are in the _brick list attribute and adds it to the view.
        Also draws the paddle onto the view when the game has started.
        
        Parameter view: The game view used in drawing.
        Precondition: view is an instance of GView"""
        
        for brick in self.getBricks():
            brick.draw(view)
        self.getPaddle().draw(view)
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def makeBricks(self):
        """Fills a one-dimensional list of bricks with brick
        object, which are all instances of class Brick. Also sets the
        color of the bricks according to the player's house.
        """
        
        self._bricks = []
        if self.getPlayerHouse() == "Gryffindor":
            BRICK_COLORS = BRICK_COLORS_G
        elif self.getPlayerHouse() == "Slytherin":
            BRICK_COLORS = BRICK_COLORS_S
        elif self.getPlayerHouse() == "Hufflepuff":
            BRICK_COLORS = BRICK_COLORS_H
        else:
            BRICK_COLORS = BRICK_COLORS_R
            
            
        for row in range(BRICK_ROWS):
            for col in range(BRICKS_IN_ROW):
                brick = Brick(left = BRICK_SEP_H/2+col*(BRICK_WIDTH+BRICK_SEP_H),
                                          top = GAME_HEIGHT-(BRICK_Y_OFFSET+
                                                             row*(BRICK_HEIGHT+BRICK_SEP_V)),
                                          width = BRICK_WIDTH,
                                          height = BRICK_HEIGHT,
                                          linecolor = BRICK_COLORS[row%len(BRICK_COLORS)],
                                          fillcolor = BRICK_COLORS[row%len(BRICK_COLORS)])
                self._bricks.append(brick)
    
    def makeBall (self):
        """Sets the ball attribute to an instance of Ball from models.py,
        thus creating the ball to be played in the game according to the constants provided.
        """
        
        self._ball = Ball(x = GAME_WIDTH/2, y=300, width = BALL_DIAMETER,
                          height = BALL_DIAMETER, fillcolor = colormodel.RGB(103,10,10))
        self._ball.velocity()
    
    def looseOneLife(self):
        """Returns: A boolean value. True if the has hit the bottom wall and has lost a life,
        False if the ball hasn't touched the bottom wall.
        """
        
        if self.getBall().hitBottomWall():
            return True
        return False
    
    def determineHouse(self):
        """Sets the player's house depending on the character's name that the
        player has been randomly assigned. This allows for the player to be informed
        about which house they are playing for, and affects the color of the bricks.
        """
        
        name = self.getPlayerName()
        if name in ["Newt Scamandar", "Cedric Diggory"]:
            self.setPlayerHouse("Hufflepuff")
        elif name in ["Draco Malfoy", "Tom Riddle", "Severus Snape", "Bellatrix Lestrange"]:
            self.setPlayerHouse("Slytherin")
        elif name in ["Luna Lovegood", "Albus Dumbledore", "Gilderoy Lockhart"]:
            self.setPlayerHouse("Ravenclaw")
        else:
            self.setPlayerHouse("Gryffindor")
    

 
