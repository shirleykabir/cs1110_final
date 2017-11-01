# breakout.py
# Sneha Kumar (sk2279), Shirley Kabir(szk4)
# DATE COMPLETED HERE
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *
import colormodel
import random


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _ctdTime [float>=0.0 to add up elapsed time since the state has been STATE_COUNTDOWN]
                total time since beginning of STATE_COUNTDOWN
                
        _numberOfLives  [int >= 0]
                        keeps track of the number of lives the player has left
        
        _endmssg        [GLabel, or None if there is no message to display]
                        the message when the game is over
                
        _pausemssg      [GLabel, or None if there is no message to display]
                        the message when the game is in STATE_PAUSED
                
        _pauseTime      [float>=0.0 to add up elapsed time since the state has been STATE_PAUSED]
                        total time since beginning of STATE_PAUSED
        
        _ctdmssg        [GLabel, or None if there is no message to display]
                        the message when the game is in STATE_COUNTDOWN
                  
        _stryTime       [float>=0.0 to add up elapsed time since the state has been STATE_STORY]
                        total time since beginning of STATE_STORY
        
        _strymssg       [GLabel, or None if there is no message to display]
                        the message when the game is in STATE_STORY
                  
        _background     [GRectangle]
                        a rectangle to change the background color in STATE_STORY
        
        _diagonAlley    [GLabel]
                        text that says "Diagon Alley", which is the goal of the game
        
        _deathlyHallows [GImage, or None if there is no image to display]
                        an image of the deathly hallows symbol in STATE_STORY
        
        _newgamemssg    [GLabel, or None if there is no message to display]
                        the message when the game is in STATE_PLAYNEWGAME
        
        _endTime        [float>=0.0 to add up elapsed time since the state has been in STATE_WON or STATE_LOST]
                        total time since beginning of STATE_WON or STATE_LOST
        
        _resKeyIsYes    [boolean]
                        True when the key pressed is "y" or "Y" to start a new game, False otherwise. 
        
        _resKeyIsNo     [boolean]
                        True when the key pressed is "n" or "N" to quit the game.
        
        _aboutmessg     [GLabel, or none if there is no message to display]
                        the message to display information about the player, which is randomly assigned
        

    """
    
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        # IMPLEMENT ME
        
        self._mssg = GLabel(text='I Open At The Close \n (Press Any Key To Begin)',
                            x=GAME_WIDTH/2, y= GAME_HEIGHT/2)
        self._mssg.font_name="harrypotter.TTF"
        self._mssg.font_size = 45
        self._state = STATE_INACTIVE
        self._game = None
        self._ctdTime = 0.0
        self._numberOfLives = NUMBER_TURNS
        self._endmssg = None
        self._pausedTime = 0.0
        self._pausemssg = None
        self._ctdmssg = None
        self._stryTime = 0.0
        self._strymssg = None
        self._background = GRectangle(x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                        width = GAME_WIDTH, height = GAME_HEIGHT,
                        linecolor = colormodel.BLACK, fillcolor = colormodel.BLACK)
        self._diagonAlley = GLabel(text='DIAGON ALLEY', x=GAME_WIDTH/2,
                        y= GAME_HEIGHT-(BRICK_Y_OFFSET+(BRICK_ROWS*(BRICK_HEIGHT+
                                                                BRICK_SEP_V)/2)))
        self._aboutmssg = None
        self._diagonAlley.linecolor = colormodel.RGB(0, 0, 0, a =  15)
        self._diagonAlley.font_name="harrypotter.TTF"
        self._diagonAlley.font_size = 5 * BRICK_ROWS
        self._deathlyHallows = None
        self._endTime = 0.0
        self._newgamemssg = None
    
    
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        *STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        *STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        *STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        *STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        STATE_WON: This is the state that the game is in when the player has hit all
        of the bricks with 3 lives. The application switches to this state only if it
        was in STATE_ACTIVE previously.
        
        STATE_LOST: This is the state that the game is in when the player does not hit
        all of the bricks with 3 lives. The application switches to this state only if
        it was in STATE_ACTIVE previously.
        
        STATE_STORY: The game switches to this state right after a key is pressed in
        STATE_INACTIVE and displays a backstory and the goal of the game.
        
        STATE_ABOUT: The game switches to this state right after it is in STATE_STORY.
        This state displays the information about the player, which is randomly
        assigned.
        
        STATE_PLAYNEWGAME: The game switches to this state after a few seconds of
        either STATE_LOST or STATE_WON to direct it to begin a new game or not.
        Depending on the player's response, the application will either start a
        new game and go into STATE_COUNTDOWN or quit.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        self.inactiveState(dt)
        self.pausedState(dt)
        self.countdownState(dt)
        self.storyState(dt)
        self.newgameState(dt)
        self.activeState(dt)
        
        if self._state == STATE_ACTIVE or self._state == STATE_COUNTDOWN:
            self._game.updatePaddle(self.input)
            
        if self._state == STATE_COUNTDOWN or self._state ==STATE_ACTIVE or self._state == STATE_PAUSED:
            if self._aboutmssg==None:
                self._aboutmssg = GLabel(text = "Welcome, " + self._game.getPlayerName() + " of " +
                                     self._game.getPlayerHouse(),  x=GAME_WIDTH/2, y= GAME_HEIGHT-(BRICK_Y_OFFSET/2))
                self._aboutmssg.font_name = "harrypotter.TTF"
                self._aboutmssg.font_size = 30
            
        self.wonState(dt)
        self.lostState(dt)
        self.changeToAskNewGame(dt)
        self.askNewGameState(dt)
    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        # IMPLEMENT ME
        self.drawingMessages()

        if self._state != STATE_LOST or self._state != STATE_WON:
            if self._mssg != None:
                self._mssg.draw(self.view)
            if self._state == STATE_STORY:
                self._background.draw(self.view)
                if self._deathlyHallows != None:
                    self._deathlyHallows.draw(self.view)
            if self._strymssg != None:
                self._strymssg.draw(self.view)
            if self._state == STATE_ACTIVE or self._state == STATE_COUNTDOWN or self._state == STATE_PAUSED:
                self._diagonAlley.draw(self.view)
                self._game.draw(self.view)
                if self._aboutmssg != None:
                    self._aboutmssg.draw(self.view)
            if self._state==STATE_ACTIVE:
                self._game.getBall().draw(self.view)
            if self._pausemssg != None:
                self._pausemssg.draw(self.view)
            if self._ctdmssg != None:
                self._ctdmssg.draw(self.view)
            
    
    
    # HELPER METHODS FOR THE STATES GO HERE
    
    
    def inactiveState(self,dt):
        """ Sets the message to none once the state changes out of STATE_INACTIVE
        and sets the next state to STATE_STORY.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)"""
        
        #Following line taken from lecture code
        curr_keys = self.input.key_count
        key_pressed = curr_keys!=0
        if key_pressed and self._state == STATE_INACTIVE:
            self._state = STATE_STORY
        if self._state != STATE_INACTIVE:
            self._mssg = None
            
    def pausedState(self,dt):
        """ Sets a timer for STATE_PAUSED and creates a message with the number
        of lives remaining in that state. Changes the state to STATE_COUNTDOWN
        once the timer in STATE_PAUSED ends.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)"""
        
        if self._state == STATE_PAUSED:
            self._pausedTime = self._pausedTime + dt
            self._pausemssg = GLabel(text= 'Number of Lives Remaining: ' +
                        str(self._numberOfLives), x=GAME_WIDTH/2, y= GAME_HEIGHT/2)
            self._pausemssg.font_name="harrypotter.TTF"
            self._pausemssg.font_size = 30
        if self._pausedTime >= 3 and self._state == STATE_PAUSED:
            self._pausemssg = None
            self._pausedTime = 0.0
            self._state = STATE_COUNTDOWN
            
    def countdownState(self,dt):
        """ Changes the state from STATE_NEWGAME to STATE_COUNTDOWN. Sets a timer
        for STATE_COUNTDOWN and creates a message counting down the seconds until
        the state changes to STATE_ACTIVE. Changes the state to STATE_ACTIVE once
        the timer in STATE_COUNTDOWN ends.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)"""
        
        if self._state == STATE_COUNTDOWN:
            self._ctdTime = self._ctdTime + dt
        if self._state == STATE_COUNTDOWN and self._ctdTime <= 3:
            self._ctdmssg = GLabel(text= str(3-int(self._ctdTime)), x=GAME_WIDTH/2,
                    y= GAME_HEIGHT/2)
            self._ctdmssg.font_name="harrypotter.TTF"
            self._ctdmssg.font_size = 50
        if self._ctdTime >= 3 and self._state == STATE_COUNTDOWN:
            self._state = STATE_ACTIVE
            self._game.makeBall()
        if self._state == STATE_NEWGAME:
            self._state = STATE_COUNTDOWN
        
            
    def storyState(self,dt):
        if self._state == STATE_STORY:
            self._stryTime = self._stryTime + dt
            self._deathlyHallows = GImage(x = GAME_WIDTH/2, y = GAME_HEIGHT-100,
                    width = 100, height = 100, source = 'deathly-hallows.png')
        if self._state == STATE_STORY and self._stryTime >= 10:
            self._state = STATE_NEWGAME
        if self._state == STATE_STORY:
            self._strymssg = GLabel(text='Congratulations on your acceptance\nto the Quidditch Council of Defense!\nDeatheaters have swarmed Diagon Alley\nand used dark magic to seal the bricks.\nUsing the wooden paddle,\nit is your job to shoot the quaffle at the\nbricks until the wall crumbles and good prevails!\nGood luck on your first mission!', x=GAME_WIDTH/2, y= GAME_HEIGHT/2, fillcolor = colormodel.BLACK)
            self._strymssg.font_name="harrypotter.TTF"
            self._strymssg.font_size = 30
            self._strymssg.linecolor = colormodel.RGB(158, 60, 51)
            
    def newgameState(self,dt):
        if self._state == STATE_NEWGAME:
            self._strymssg = None
            self._game = Play()
            
    def activeState(self,dt):
        if self._state == STATE_ACTIVE:
            self._ctdmssg = None
            self._game.updateBall()
            if self._game.getBricks() == []:
                self._state = STATE_WON
            if self._game.looseOneLife():
                self._numberOfLives -= 1
                if self._numberOfLives == 1 or self._numberOfLives == 2:
                    self._state = STATE_PAUSED
                elif self._numberOfLives == 0:
                    self._state = STATE_LOST
                    
    def wonState(self,dt):
        if self._state == STATE_WON:
            self._endTime = self._endTime + dt
            quote = self.makeQuote()
            self._endmssg = GLabel(text= quote + '\nCongratulations, you\'ve succeeded\nin your mission!', x=GAME_WIDTH/2, y= GAME_HEIGHT/2)
            self._endmssg.font_name="harrypotter.TTF"
            self._endmssg.font_size = 35.0
        
    def lostState(self,dt):
        if self._state == STATE_LOST:
            self._endTime = self._endTime + dt
            findSpace = (self._game.getPlayerName()).find(" ")
            if findSpace != -1:
                lastName = (self._game.getPlayerName())[findSpace+1:]
            self._endmssg = GLabel(text='Better luck next time, ' + lastName, x=GAME_WIDTH/2, y= GAME_HEIGHT/2)
            self._endmssg.font_name="harrypotter.TTF"
            self._endmssg.font_size = 35.0

    
    def changeToAskNewGame(self, dt):
        
        if (self._state == STATE_WON or self._state == STATE_LOST) and self._endTime >= 4.5:
            self._state = STATE_PLAYNEWGAME
            self._endmssg = None
            self._endTime = 0.0
    
    def askNewGameState(self, dt) :
        """
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        
        self._resKeyIsYes = self.input.is_key_down("y")
        self._resKeyIsNo = self.input.is_key_down("n")
        if self._state == STATE_PLAYNEWGAME:
            self._newgamemssg = GLabel(text='Want A New Mission from the QCD?\n - Press "Y" for New Game\nor\n Press "N" to Leave the Wizarding World', x=GAME_WIDTH/2, y= GAME_HEIGHT/2)
            self._newgamemssg.font_name="harrypotter.TTF"
            self._newgamemssg.font_size = 35.0
            if self._resKeyIsYes:
                self._newgamemssg = None
                self._game.makeBricks()
                self._ctdTime = 0.0
                self._numberOfLives = NUMBER_TURNS
                self._state = STATE_COUNTDOWN
            elif self._resKeyIsNo:
                self.stop()
                
    def makeQuote(self):
        if self._game.getPlayerHouse() == "Ravenclaw":
            return QUOTES[0]
        elif self._game.getPlayerHouse() == "Gryffindor":
            return QUOTES[1]
        elif self._game.getPlayerHouse() == "Hufflepuff":
            return QUOTES[2]
        else:
            return QUOTES[3]
        
    def drawingMessages(self):
        if self._endmssg != None:
            self._endmssg.draw(self.view)
        if self._newgamemssg != None:
            self._newgamemssg.draw(self.view) 

