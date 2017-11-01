# models.py
# Sneha Kumar (sk2279), Shirley Kabir(szk4)
# December 7th, 2016
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    
    def collidesWithPaddle(self,ball):
        """Returns: A boolean; returns True if the ball has hit the paddle
        at one of the three points in the ball, False otherwise. 
        
        Parameter ball: The ball to check whether it has hit the paddle or not.
        Precondition: ball is a Ball object
        """
        
        if self.contains(ball.x, ball.y-ball.height/2):
            return True
        elif self.contains(ball.x+ball.width/2, ball.y-ball.height/2):
            return True
        elif self.contains(ball.x-ball.width/2, ball.y-ball.height/2):
            return True
        return False
    
    def moveAfterPaddle(self,ball):
        """If the ball has collided with the paddle, it bounces off at a random x
        velocity and a negative y velocity to continue to hit the other bricks.
        
        Parameter ball: The ball to which the changing velocity belongs
        Precondition: ball is a Ball object
        """
        
        if self.collidesWithPaddle(ball):
            if ball.getVerticalVelocity() <= 0:
                ball.setVerticalVelocity(ball.getVerticalVelocity() * -1)
                ball.setHorizontalVelocity(ball.getHorizontalVelocity() * random.choice([-1, 1])) 


class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # METHOD TO CHECK FOR COLLISION
    def collidesWithBrick(self, ball):
        """Returns: A boolean; returns True ball has hit a
        brick in the list of bricks at one of the eight points, False otherwise.
        
        Parameter ball: The ball to check whether it has hit a brick or not.
        Precondition: ball is a Ball object
        """
        
        if self.contains(ball.x-ball.width/2, ball.y-ball.height/2):
            return True
        elif self.contains(ball.x+ball.width/2, ball.y-ball.height/2):
            return True
        elif self.contains(ball.x-ball.width/2, ball.y+ball.height/2):
            return True
        elif self.contains(ball.x+ball.width/2, ball.y+ball.height/2):
            return True
        elif self.contains(ball.x, ball.y-ball.height/2):
            return True
        elif self.contains(ball.x, ball.y+ball.height/2):
            return True
        elif self.contains(ball.x-ball.width/2, ball.y):
            return True
        elif self.contains(ball.x+ball.width/2, ball.y):
            return True
        return False
    
    def moveAfterBrick(self, ball):
        """Moves the ball so that it bounces off the brick once it has
        collided and makes a sound simultaneously.
        
        Parameter ball: The ball to which the changing velocity belongs
        Precondition: ball is a Ball object
        """
        
        # .WAV file was found on freesound.org
        bounceSound = Sound('basketbounce.wav')
        ball.setVerticalVelocity(ball.getVerticalVelocity() * -1)
        bounceSound.play()
    
    
class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getHorizontalVelocity(self):
        """Returns: The horizontal velocity of the game.
        
        This getter method is to protect access to the x-velocity.
        """
        
        return self._vx
    
    def getVerticalVelocity(self):
        """Returns: The vertical velocity of the game.
        
        This getter method is to protect access to the y-velocity.
        """
        
        return self._vy
    
    def setVerticalVelocity(self, value):
        """Sets the vertical velocity of the ball to the value provided.
        
        Parameter value: The new x-velocity.
        Precondition: value is a float type.
        """
        
        self._vy = value
        
    def setHorizontalVelocity(self, value):
        """Sets the horizontal velocity of the ball to the value provided.
        
        Parameter value: The new y-velocity.
        Precondition: value is a float type.
        """
        
        self._vx = value
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def velocity(self):
        """Sets the vertical velocity to a float and randomly picks and
        assigns the horizontal velocity."""
        
        self._vy = -5.0
        self._vx = random.uniform(1.0,5.0) 
        self._vx = self._vx * random.choice([-1, 1])
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self):
        """Modifies the vertical and horizontal velocities of the ball if it has hit one of the walls,
        excluding the bottom wall."""
        
        self.x = self.x + self.getHorizontalVelocity()
        self.y = self.y + self.getVerticalVelocity()
        self.changeHorizontalVelocity()
        self.changeVerticalVelocity()
        
            
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def changeHorizontalVelocity(self):
        """Helper function to change the horizontal velocity of the ball if it has collided
        with one of the walls, excluding the bottom wall.
        """
        
        if (self.x + self.width/2) >= GAME_WIDTH or (self.x - self.width/2)<= 0:
            self._vx = self._vx * -1
            self.x = self.x + self.getHorizontalVelocity()
            
    def changeVerticalVelocity(self):
        """Helper function to change the vertical velocity of the ball if it has collided
        with one of the walls, excluding the bottom wall.
        """
        
        if (self.y + self.height/2) >= GAME_HEIGHT:
            self._vy = self._vy * -1
            self.y = self.y + self.getVerticalVelocity()
    
    def hitBottomWall(self):
        """Returns: A boolean; True of the ball has hit the bottom wall, False otherwise.
        Helper function to change the number of lives remaining in the game."""
        
        if(self.y-self.height/2 <= 0):
            return True  
        return False
