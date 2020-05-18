import pygame
import random
import os
import time

class Boundary:
    '''Generate pygame display window.
    
    Args:
        width (int): width of display in number of pixels
        height(int): height of display in number of pixels
    '''
    back_ground = pygame.image.load('Background_images/p.png')

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Interstellar Escort')


class Mothership:
    '''Mothership object is displayed at the bottom of screen and the objective is to protect it.

    Class Attributes:
        image (pygame image): 50x500 image displayed onscreen

    Attributes:
        x (int): x coordinate image location
        y (int): y coordinate image location
        health_amt (int): initial health amount
        damage_taken (int): initial damage amount
        total (int): combination of health and damage amounts
        hbar_x (int): x coordinate of health bar
        hbar_y (int): y coordinate of health bar
        hbar_length (int): length of health bar (constant for calcuation purposes)
        health_width int(int): ratio of remaining health over total, multiplied by health bar length
    '''
    image = pygame.image.load('Mothership/mothership_3_2.png')

    def __init__(self):
        self.x = 0
        self.y = 650
        self.health_amt = 1000
        self.damage_taken = 0
        self.total = self.health_amt + self.damage_taken
        self.hbar_x = 50
        self.hbar_y = 690
        self.hbar_length = 450 - self.hbar_x
        self.health_width = round(self.hbar_length*(self.health_amt/self.total))
        #self.damage_width = round(self.hbar_length*(self.damage_taken/self.total))
        
    def update_damage(self):
        '''Update instance's health amount and width of health bars'''
        if self.health_amt > 1000: # if health is above initial amt of 1000 due to powerup reduce in size to original
            self.health_amt = 1000    
        self.health_width = round(self.hbar_length*(self.health_amt/self.total))

    def draw(self, window): 
        '''Draw sprite and health bars to screen
        
        Args:
            window (Boundary obj): window attribute of Boundary object
        '''
        window.blit(Mothership.image, (int(self.x), int(self.y)))
        
        # Damage bar is constant length. Covered over by health bar.
        pygame.draw.rect(window, (255,0,0), (self.hbar_x, self.hbar_y, self.hbar_length, 7)) 
        
        # Draw over damage bar. Damage bar is revealed as health is depleted.
        if self.health_amt > 0: 
            pygame.draw.rect(window, (0,255,0),(self.hbar_x, self.hbar_y, self.health_width, 7)) 


class Character:
    '''Character class is main sprite (spaceship) for this game.

    Class Attributes
        center_images (pygame image): images displaying ship in upright postion
        strafing_right_images (pygame image): intermediate images for right turns
        strage_right_on (pygame image): final images for right turns
        strafing_left_images (pygame image): intermediate images for left turns
        strafe_left_on (pygame image): final images for left turns

    Attributes
        width (int): width of character image in pixels
        height (int): height of character image in pixels
        x (int): initial x coordinate position of character
        y (int): initial y coordinate position of character
        velocity (int): rate at which character moves from left to right
        left (bool): indicate initial movement setting (for image displaying purposes)
        right (bool): indicate initial movement setting
        center (bool): indicate initial movement setting
    '''
    # images used when no keys are pressed
    center_images = [pygame.image.load('main_sprite/planes_02A-center1.png'), pygame.image.load('main_sprite/planes_02A-center2.png'), pygame.image.load('main_sprite/planes_02A-center3.png'), pygame.image.load('main_sprite/planes_02A-center4.png')]
    # images used inbetween full strafe right
    strafing_right_images = [pygame.image.load('main_sprite/planes_02A-strafe_right5.png'),pygame.image.load('main_sprite/planes_02A-strafe_right6.png'),pygame.image.load('main_sprite/planes_02A-strafe_right7.png'),pygame.image.load('main_sprite/planes_02A-strafe_right8.png')]
    # images used at full right strafe
    strafe_right_on = [pygame.image.load('main_sprite/planes_02A-R9.png'), pygame.image.load('main_sprite/planes_02A-R10.png'), pygame.image.load('main_sprite/planes_02A-R11.png'), pygame.image.load('main_sprite/planes_02A-R12.png')]
    # images used inbetween full strafe left
    strafing_left_images = [pygame.image.load('main_sprite/planes_02A-strafe_left5.png'), pygame.image.load('main_sprite/planes_02A-strafe_left6.png'), pygame.image.load('main_sprite/planes_02A-strafe_left7.png'), pygame.image.load('main_sprite/planes_02A-strafe_left8.png')]
    # images used at full left strafe
    strafe_left_on = [pygame.image.load('main_sprite/planes_02A-L9.png'), pygame.image.load('main_sprite/planes_02A-L10.png'), pygame.image.load('main_sprite/planes_02A-L11.png'), pygame.image.load('main_sprite/planes_02A-L12.png')]

    def __init__(self):
        self.width = 96
        self.height = 96
        self.x = 200
        self.y = 540
        self.velocity = 5
        self.left = False                                           # Initial movement position states of sprite
        self.right = False                                          
        self.center = True
    
    def draw(self, left_right_frame, center_frame, most_recent_key, window):
        '''Draw the mainsprite to the screen

        Args
            left_right_frame (int): incrementing number that controls which frame is selected for displaying when moving right/left
            center_frame (int): incrementing number that controls which frame is selected when not turning
            most_recent_key (str): most recently pressed movement key. 
            window (Boundary obj): screen on which image is displayed

        '''
        if self.center == True:
            if left_right_frame < 4:
                if most_recent_key == 'r':
                    window.blit(self.strafing_right_images[left_right_frame], 
                               (self.x, self.y))        # level out spaceship upon returning to center
                elif most_recent_key == 'l':
                    window.blit(self.strafing_left_images[left_right_frame], 
                               (self.x, self.y))        # level out spacehip upon returning to center
            else:    
                window.blit(self.center_images[center_frame], 
                           (self.x, self.y))            # iterate through displaying center images

        elif self.right == True:
            if left_right_frame < 4:                    # first 4 frames are transition state
                window.blit(self.strafing_right_images[left_right_frame], 
                           (self.x, self.y))            # draw strafe right transition
            else:
                window.blit(self.strafe_right_on[left_right_frame % 4], 
                           (self.x, self.y))            # draw final strafe right
            
        elif self.left == True:
            if left_right_frame < 4:                    # first 4 frames are transition state
                window.blit(self.strafing_left_images[left_right_frame], 
                           (self.x, self.y))            # draw strafe left transition
            else:
                window.blit(self.strafe_left_on[left_right_frame % 4], 
                           (self.x, self.y))            # draw final strafe left
        
    def move_left(self, boundary):
        '''Move character in the left direction by velocity amount
        Args
            boundary (Boundary obj): Boundary width is used to know movement limit
        '''
        if self.x > 0:                                  # keeping x coordinate within the bounds of the screen
            self.x = self.x - self.velocity             # move by velocity amt

    def move_right(self, boundary):
        '''Move character in the right direction by velocity amount
        
        Args
            boundary (Boundary obj): Boundary width is used to know movement limit 
        '''
        if self.x < boundary.width - self.width:
            self.x = self.x + self.velocity

    def shoot(self, shot_type):
        '''Generate ShooterObject object at the center position of the main sprite

        Args
            shot_type (str): specifies the type of shot generated. Could be used to change shot types in future use.
        '''
        # generate shot object at current sprite location, in the middle of the sprite
        ShooterObject.shots_queue.append(ShooterObject(shot_type, (self.x + (self.width/2)), self.y)) 


class Asteroid:
    '''Asteroid class generates asteroids images above the display height and progresses them downward

    Class Attributes
        astoird_images (dict): dictionary of asteroid pygame images with keys specifying the size of the asteroid
        width_options (list): list containing the various width options
        ast_diff_setting (dict): dictionary for difficulty setting.
            Keys are levels of difficult and values are average number of game loops per asteroid generation 
        current_setting (int): current difficulty setting
        maximum_asteroid_amount (int): limit on the current number of existing asteroid

    Attributes
        width (int): width of asteroid choosen
        color_option (int): color of asteroid choosen
        y (int): y coordinate of asteroid spawn
        x (int): x coordinate of asteroid spawn
        velocity (int): speed at which asteroid progresses down screen
        damage_taken (int): amount of damage sustained
        health_amt (int): amount of health
        damage (int): amount of damage dealt 
        hbar_length (int): length of health bar
        initial_health_width (int): length of health bar as a constant
        destruction method (None): method by which the asteroid has been destroyed

    '''
    asteroid_images = {50:[pygame.image.load('Asteroids/res50.png'),pygame.image.load('Asteroids/res50_1.png'),pygame.image.load('Asteroids/res50_2.png'),pygame.image.load('Asteroids/res50_3.png'),pygame.image.load('Asteroids/res50_4.png')],\
        60:[pygame.image.load('Asteroids/res60.png'),pygame.image.load('Asteroids/res60_1.png'),pygame.image.load('Asteroids/res60_2.png'),pygame.image.load('Asteroids/res60_3.png'),pygame.image.load('Asteroids/res60_4.png')],\
            70:[pygame.image.load('Asteroids/res70.png'),pygame.image.load('Asteroids/res70_1.png'),pygame.image.load('Asteroids/res70_2.png'),pygame.image.load('Asteroids/res70_3.png'),pygame.image.load('Asteroids/res70_4.png')],\
                80:[pygame.image.load('Asteroids/res80.png'),pygame.image.load('Asteroids/res80_1.png'),pygame.image.load('Asteroids/res80_2.png'),pygame.image.load('Asteroids/res80_3.png'),pygame.image.load('Asteroids/res80_4.png')],\
                    90:[pygame.image.load('Asteroids/res90.png'),pygame.image.load('Asteroids/res90_1.png'),pygame.image.load('Asteroids/res90_2.png'),pygame.image.load('Asteroids/res90_3.png'),pygame.image.load('Asteroids/res90_4.png')],\
                        100:[pygame.image.load('Asteroids/res100.png'),pygame.image.load('Asteroids/res100_1.png'),pygame.image.load('Asteroids/res100_2.png'),pygame.image.load('Asteroids/res100_3.png'),pygame.image.load('Asteroids/res100_4.png')]}
    
    width_options = [x for x in range(50,110,10)]
    asteroid_lst = []
    ast_diff_setting = {1:1000, 2:800, 3: 600, 4: 400, 5:200, 6:100, 7:50}
    current_setting = 6
    maximum_asteroid_amount = 9

    def __init__(self):
        self.width = random.choice(Asteroid.width_options)  # randomly choosing width option from width_options
        self.color_option = random.randint(0,4)             # randomly choosing an index number to pick from various images
        self.y = self.width*-1                              # spawns asteroids above game window
        self.x = random.randrange(50, 500 - self.width)     # asteroid spawn anywhere in x direction within game boundaries
        if self.width < 80:                                 # velocity is loosley tied to width
            self.velocity = random.randint(2,3)
        else:
            self.velocity = random.randint(1,2)                       
        self.damage_taken = 0                               # the total health remains unchanged and is used to generate health bar ratio
        self.health_amt = self.width*2                      # health amount is directly related to the size of the asteroid
        self.damage = self.width * 2                        # damage dealt by asteroid is tied to size 
        self.hbar_length = round(self.width * 0.75)         # constant length (should add up from the summations of health and damage bar widths)
        self.hbar = round(self.hbar_length * 
                         (self.health_amt/(self.health_amt + self.damage_taken))) # hbar length multiplied by percentage remaining
        self.initial_health_width = self.hbar               # new variable so that changing hbar will not affect the initial length of health bar
        self.destruction_method = None                      # either destroyed by negative health or making contact with mothership
        Asteroid.asteroid_lst.append(self)

    def draw_asteroid(self, surface):
        '''Draw asteroid on screen
        
        Args
            surface (boundary obj): surface upon which the asteroid is drawn
        '''
        surface.blit(Asteroid.asteroid_images[self.width][self.color_option], (self.x, self.y))

        # creating damage bar (red)
        if self.damage_taken > 0:
            pygame.draw.rect(surface, (255,0,0), (self.x + round(self.width*0.1), round(self.y + self.width/2), 
                                                                self.initial_health_width, 7)) 
        # avialable health (green) is dependent on the ratio of health remaining to damage taken
        pygame.draw.rect(surface, (0,255,0), (self.x + round(self.width*0.1), round(self.y + self.width/2), self.hbar, 7))
        
    def update_health_bars(self):
        '''Update health bars'''
        self.hbar = round(self.hbar_length * 
                        (self.health_amt/(self.health_amt + self.damage_taken))) # length multiplied by fraction of health remaining

    def progress_down(self):
        '''Move asteroids down screen'''
        self.y += self.velocity

    def generate_explosion(self):
        '''Generate Explosion object at last coordinates'''
        Explosion(self.x, self.y, self.width, self.destruction_method) #explosion occurs at asteroids last location

    def __del__(self):
        '''Delete Asteroid object'''
        pass


class TimedPowerUp:
    '''TimedPowerUp creates powerups, progresses them down screen, and grants main sprite effects that have a temporal component

    Class Attributes
        power_ups (dict): dictionary containing pygame images for the two different powerup images
        power_up_optiosn (list): list contianing powerup options
        current_powerups (list): list containing all TimedPowerUp objects that currently exist
        activated (bool): determination if powerup has been activated
        current_option (none): power up that was most recently generated

    Args
        p_type (str): the name of TimedPowerUp that is being generated

    Attributes
        width (int): width of powerup 
        height (int): height of powerup 
        x (int): x coordinate spawn location
        y (int): y coordinate spawn location
        velocity (int): movement speed
        font_color (tuple): RGB value of font color
        powerup_font (SysFont obj): pygame SysFont() contains font type, font size, and bold
        powerup_text (pygame text obj): text generated
        powerup_display_timer (int): timer used to mark how long the effect name is displayed on screen
        effect_timer (int): timer used to mark long long the effect has been active
        powerup_duration (int): duration of power up effect
    '''

    power_ups = {'Insta-Kill':pygame.image.load('powerups/icon-powerup.png'), 'Double XP':pygame.image.load('powerups/icon-special.png')}
    power_up_options = ['Insta-Kill', 'Double XP']
    current_powerups = []
    activated = False
    current_option = None

    def __init__(self, p_type):
        self.width = 25
        self.height = 20
        self.x = random.randint(25, 500 - (2*self.width))           # x coordinate choosen at random, spaced slightly from screen sides
        self.y = -1 * self.height                                   # spawn right above upper boundry
        self.velocity = 3
        self.font_color = (255,255,255)                             # color white
        self.powerup_font = pygame.font.SysFont('comicsans', 80, 1) # Comicsans, 80 font height, and bold
        TimedPowerUp.current_option = p_type                        # setting class attribute to most current generated powerup
        self.powerup_text = self.powerup_font.render(p_type, 1, self.font_color)
        self.powerup_display_timer = 0
        self.effect_timer = 0
        self.powerup_duration = 550                                 # duration is a set at 550 game loops
        TimedPowerUp.current_powerups.append(self)                  # appending instance to list of current TimedPowerUp objects

    def draw(self, window):
        '''Draw powerup image on screen

        Args
            window (Boundary obj): surface to which the image is drawn
        '''
        if TimedPowerUp.activated == False: # Only display the powerup image if it hasn't been activated yet
            window.blit(TimedPowerUp.power_ups[TimedPowerUp.current_option], (self.x, self.y))

        elif TimedPowerUp.activated == True: # If activated, no longer display image. Display text instead
            window.blit(self.powerup_text, (500//2 - self.powerup_text.get_width()//2, 700//2 - 100))

    def progress(self):
        '''Progress powerup down screen'''
        self.y += self.velocity

    def __del__(self):
        '''Delete TimedPowerUp object'''
        pass


class Health_PowerUp:
    '''Generates health powerups which have the one time effect of return some health to the Mothership

    Class Attributes
        health_image (pygame image): image for health powerup
        current_powerups (list): list containing all currently existing instances of Health_PowerUp

    Attributes
        width (int): width of power up
        height (int): height of power up
        x (int): x coordinate of spawn location
        y (int): y coordinate of spawn location
        health_add (int): amount of health granted upon activation
        velocity (int): movement speed
        activated (bool): whether or not the powerup has been activated
        font_color (tuple): RGB value for font color
        powerup_font (SysFont obj): font information; font type, size, bold
        powerup_text (pygame text): text to be displayed
        powerup_display_timer (int): timer for how long the text has been displayed to screen
    '''
    health_image = pygame.image.load('powerups/icon-health.png')
    current_powerups = []

    def __init__(self):
        self.width = 25
        self.height = 20
        self.x = random.randint(25, 500 - (2*self.width))   # x coordinate choosen at random with slight spacing from walls
        self.y = -1 * self.height                           # spawn right above upper boundry
        self.health_add = 250                               # amount of health returned to mothership
        self.velocity = 3
        self.activated = False                              # whether or not the powerup has been captured by main sprite
        self.font_color = (255,255,255)
        self.powerup_font = pygame.font.SysFont('comicsans', 80, 1)
        self.powerup_text = self.powerup_font.render('Health' + ' +' + str(self.health_add), 1, self.font_color)
        self.powerup_display_timer = 0
        Health_PowerUp.current_powerups.append(self)

    def draw(self, window):
        '''Display health powerup image and text on screen

        Args
            windwo (Boundary obj): surface to which the image is drawn
        '''
        if self.activated == False: # if not activated yet, only display image and not text
            window.blit(Health_PowerUp.health_image, (self.x, self.y))

        if self.activated == True: # if activated, no longer display image and display text in the middle of the screen
            window.blit(self.powerup_text, (500//2 - self.powerup_text.get_width()//2, 700//2 - 100))

    def progress(self):
        '''Progress health powerup down screen'''
        self.y += self.velocity

    def __del__(self):
        '''Delete Health_PowerUp object'''
        pass


class Explosion:
    '''Generates explosion upon destruction of an asteroid

    Class Attributes
        explosion_lst (list): list containing all currently existing instances of the Explosion class
        explostion_images (list): list containin pygame images of various explosion stages

    Args
        x (int): x coordinate of where explosion should occur
        y (int): y coordinate of where explosion should occure
        score_incr (int): amount by which score should incrase upon user destruction
        method (str): string detailing how the asteroid was destroyed

    Attributes
        x (int): storage of input x argument
        y (int): storage of input y argument
        current_frame (int): number detailing which image is to be displayed
        font (pygame font): font information (font type, size, bold)
        font_color (tuple): RGB color value for font
        ast_width (int): width of asteroid that generated explosion
        score_incrase (int): amount by which the user's score will increase
        text (pygame text): score increase text to be displayed to screen
        text_loc (tuple): location of text on screen (x, y, width, height)
        method (str): storage of input argument method
        count (int): timer used to control displaying of score increase text to screen
        explosion_sound (pygame Sound): sound generated upon explosion
    '''

    explosion_lst = []
    explosion_images = [pygame.image.load(f'explosions/explosion-{x}.png') for x in range(1,12)]

    def __init__(self, x, y, score_incr, method):
        self.x = x
        self.y = y
        self.current_frame = 0
        self.font = pygame.font.SysFont('comicsans',30,True)
        self.font_color = (255,255,255)
        self.ast_width = score_incr
        # if a TimedPowerup is active and it is 'Double XP' then the score_increase value is double
        if (TimedPowerUp.activated == True) and (TimedPowerUp.current_option == 'Double XP'): 
            self.score_increase = score_incr*2
        else:
            self.score_increase = score_incr
        self.text = self.font.render(('+'+str(self.score_increase)), 1, self.font_color)
        # text location is in middle of asteroid and adjusted for text height and width
        self.text_loc = ((self.x + (self.ast_width//2) - (self.text.get_width()//2)), 
                        (self.y + (self.ast_width//2) + (self.text.get_height()//2)))
        self.method = method
        self.count = 1 # timer used to display score increase 
        self.explosion_sound = pygame.mixer.Sound('audio/Explosion+1.wav')
        self.explosion_sound.play()
        Explosion.explosion_lst.append(self)

    def draw(self,window):
        '''Draw explosion image and text to screen
        
        Args
            window (Boundary obj): surface to which image is displayed
        '''
        self.count += 1 # increment count to know how many times draw() has been called
        window.blit(Explosion.explosion_images[self.current_frame], (self.x, self.y))

        if self.method == 'negative health':    # indicates that asteroid was destroyed via user
            if self.count % 3 == 0:             # only display text every three calls to draw(). Gives fading effect          
                window.blit(self.text, self.text_loc)

    def __del__(self):
        '''Delete Explosion object'''
        pass
    

class ShooterObject:
    '''Shots generated py main sprite, progress up screen, and destroy asteroid

    Class Attributes
        Shots_queue (list): list containing all currently existing instances of the ShooterObject class
        shot_rate (int): rate in frames per shot

    Args
        shot_type (str): designates the type of shot and subsequent attributes that go along with that shot type
        ship_x_position (int): x coordinate of position of ship upon generation of shot
        ship_y_position (int): y coordinate of position of ship upon generation og shot

    Attributes
        shot_type (str): storage of input arguement shot_type
        width (int): width of shot in pixels
        height (int): height of object in pixels
        color (tuple): RGB value of shot color
        velo (int): movement speed of shot
        damage(int): damage amount delivered to asteroids
        hit (bool): determine whether a shot has made contact with an asteroid
        start_y (int): starting point of line that is a shot
        end_y (int): ending point of a line that is a shot
        start_x (int): starting x coordinate of a shot

    '''
    shots_queue = []            # shots generated stored here.
    shot_rate = 15              # called with modulo operator in while loop to generate shots every so many loops. lower to increase                                              

    def __init__(self, shot_type, ship_x_position, ship_y_position):
        self.shot_type = shot_type
        if self.shot_type == 'normal':
            self.width = 3
            self.height = 10
            self.color = (255,255,255)
            self.velo = 3
            self.damage = 20
        self.hit = False                                    # tells whether bullet has collided with an object
        self.start_y = ship_y_position + 25                 # y position of ship + 25 to move closer to ship
        self.end_y = self.start_y - self.height             # difference equal to shot height
        self.start_x = ship_x_position                      # tying x coord position to that of the ship
       
    def draw_line(self, surface):
        '''Draw line on screen
        
        Args
            surface (Boundary obj): surface to which the image is drawn
        '''                   
        pygame.draw.line(surface, self.color, (int(self.start_x), int(self.start_y)), 
                        (int(self.start_x), int(self.start_y) - self.height), self.width)

    def progress(self):
        '''Progress shot up screen'''
        # move both the start and end y position by the velocity amount
        self.start_y -= self.velo
        self.end_y -= self.velo

    def __del__(self):
        '''Delete ShooterObject instance'''
        pass


class Score:
    '''Keep score and display score in upper right hand corner of screen

    Attributes
        score (int): initial score
        x (int): x coordinate for displaying score text
        y (int): y coordinate for displaying score text
        score_lenth (int): current length of the score in terms of digits
        color (tuple): RGB value of score text
        font (pygame font): font information; font type, size, bold
    '''
    def __init__(self):
        self.score = 0
        self.x = 470
        self.y = 10
        self.score_length = 1
        self.color = (255,255,255)
        self.font = pygame.font.SysFont('comicsans', 30, True)
        
    def shift_score(self):
        '''Shift score over by 10'''
        self.x -= 10
    
    def draw_score(self, window):
        '''Draw score in upper right hand corner of screen

        Args
            window (Boundary obj): surface to which the score is displayed
        '''
        # if the length of the current score isn't equal to the previously set score length, an addtional column has been added
        if len(str(self.score)) != self.score_length: 
            self.score_length = len(str(self.score))    # reseting score length to new length
            self.shift_score()                          # shifting text over 

        self.text = self.font.render(str(self.score), 1, self.color) # rendering text
        window.blit(self.text, (self.x, self.y)) # displaying text


class Credits:
    '''Credits are composed of end game messages and high scores, displayed at the end of the game

    Args
        score (int): Accumulated score from the game just played

    Attributes
        score (int): storage for input arguemnt score
        color (tuple): RGB color value for displayed text
        messages (list): list of various end game messages to be displayed
        fonts (list): list of pygame fonts of various sizes
        texts (list): list of rendered texts, generated from fonts and messages
        text_widths (list): list of widths of text
        text_heights (list): list of heights of text
        x (int): x coordinate for text
        y (int): y coordinate for text
        file_contents (list): storage for highscores.txt
        file (file obj): file object of highscores.txt in 'r' mode
        outfile (file obj): creating new file object of highscores.txt in 'w' mode
    '''
    def __init__(self, score):
        self.score = score
        self.color = (255,255,255)
        self.messages = ['GAME OVER', f'Your Score: {self.score}', 'Press any key to play again', 'High Scores:']
        self.fonts = [pygame.font.SysFont('comicsans', 100, True), pygame.font.SysFont('comicsans', 50, True),
                    pygame.font.SysFont('comicsans', 30, True)]
        self.texts = [self.fonts[0].render(self.messages[0], 1, self.color), self.fonts[1].render(self.messages[1], 1, self.color),
                    self.fonts[2].render(self.messages[2], 1, self.color), self.fonts[1].render(self.messages[3], 1, self.color)]
        self.text_widths = [self.texts[0].get_width(), self.texts[1].get_width(), self.texts[2].get_width(), self.texts[3].get_width()]
        self.text_heights = [self.texts[0].get_height(), self.texts[1].get_height(), self.texts[2].get_height(), self.texts[3].get_height()]
        self.x = 250
        self.y = 200
        self.file_contents = []                     # if highscores.txt does not exist then file_contents will remain empty
        if os.path.exists('highscores.txt'):        # if highscores exist then read into file_contents
            self.file = open('highscores.txt', 'r')
            self.file_contents = self.file.readlines() 
            self.file.close()
        self.outfile = open('highscores.txt', 'w')  # open up file in 'w' under same name to overwrite scores in new order

    def write_highscores(self):
        '''Determine if current score is high score and write to outfile'';
        '''
        self.file_contents.append(str(self.score) + '\n')               # appending new score to file_contents
        self.file_contents.sort(key=(lambda x: int(x)) ,reverse=True)   # mapping each entry to int() and then sorting
        if len(self.file_contents) == 6:                                
            self.file_contents = self.file_contents[:-1]                # deprecate score list if it has reached max length
        for line in self.file_contents:
            self.outfile.write(line)                                    # writing to outfile for permanent storage
        self.outfile.close()
        
    def display_credits(self, window):
        '''Display all end game text and contents of highscores file

        Args
            window (Boundary obj): surface to which all text is displayed
        '''
        window.blit(self.texts[0], (self.x - self.text_widths[0]//2, self.y - self.text_heights[0]//2 - 50))
        window.blit(self.texts[1], (self.x - self.text_widths[1]//2, self.y - self.text_heights[1]//2 + self.text_heights[0] - 30))
        window.blit(self.texts[2], (self.x - self.text_widths[2]//2, 650))
        window.blit(self.texts[3], (self.x - self.text_widths[3]//2, 300))

        self.init_score_pos = 350
        for score in self.file_contents:
            self.f = pygame.font.SysFont('comicsans', 30, True)
            self.t = self.f.render(score[:-1], 1, self.color)   # deprecate end of score so that \n characters aren't blitted to screen

            window.blit(self.t, (self.x - self.t.get_width()//2, self.init_score_pos))
            self.init_score_pos += 40                           # iteratively move score position down screen


class GameStart:
    '''Controls game loop and all functions within game loop; collisions, drawing, generating objects, key presses.

    Attributes
        clock (pygmae Clock obj): pygame clock object for controlling game rate
        quit (bool): check if quit point during opening scene if used
        run (bool): control enter and exit of game loop
        display (Boundary obj): Creation of game window and dimension
        opening_scene(bool): control enter and exit of opening scene
        music (pygame music): game play music
        main_sprite (Character obj): main character 
        mothership (Mothership obj): mothership character
        score (Score obj): score object
        count (int): count of current overall game loop
        center_frame (int): counter telling which center image to be displayed 
        left_right_frame (int): counter telling which left/right image to be displayed
        powerup_health_timer (int): cooldown timer for health power ups
        powerup_timer (int): cooldown timer for remaining powerups
        next_frame (time obj): time object for moving between main character frames
        most_recent_key (none): contains most recently pressed key; 'l' or 'r'
    '''
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.quit = False
        self.run = True
        self.display = Boundary(500, 700)                           # Game Boundary and Window dimensions disgnation
        self.opening_scene = True
        self.open_scene()                                           # Call opening scene after creating game window and before characer objs are created
        if self.quit == False:                                      # Opening scene offers quit point. Need to check here
            
            self.music = pygame.mixer.music.load('audio/Battle-SilverMoon.mp3')
            pygame.mixer.music.play(-1)                                 
            self.main_sprite = Character()                              # initialize main sprite
            self.mothership = Mothership()                              # initialize mothership
            self.score = Score()
            self.count = 0                                              # count running so that every X amount of loops, do Y
            self.center_frame = 0
            self.left_right_frame = 0
            self.powerup_health_timer = 0                               # two seperate timers for health powerups vs. other powerups
            self.powerup_timer = 0                                      # 
            self.next_frame = time.time()
            self.most_recent_key = None                                 # input 'l' or 'r' depending on which directional was last used.                                

            while self.run:
                self.clock.tick(60)                                     # controls FPS

                if time.time() > self.next_frame:
                    self.center_frame  = (self.center_frame + 1)%4      # rotate through four static images
                    self.next_frame += .03                              # bumps self-made frame clock by 30ms (will only display new every 30)
                    self.left_right_frame += 1

                self.handle_key_presses()                               
                
                self.generate_shots()                                   # generate ShooterObjects 
                
                # only call if less than the max amount.
                if len(Asteroid.asteroid_lst) < Asteroid.maximum_asteroid_amount: 
                    self.generate_asteroids()
                
                self.generate_powerup()                                 
                
                self.handle_collisions()             
                
                if self.count % 5 == 0:
                    self.score.score += 1                               # score increase every 5 loops. 

                self.redraw_window()
                self.count += 1                                         # increment loop count
                
                if self.mothership.health_amt <= 0:                      # end game if mothership has 0 or negative health
                    self.end_game()
                    break

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        pygame.quit()
            
    def open_scene(self):
        '''Display opening scene prior to entering game loop
        
        Attributes
            open_music (pygame music): pygame music played at opening scene
            color (tuple): RGB color value of font
            fonts (list): pygame fonts for various texts
            titles (list): title for opening scene
            title_location (int): y coordinate for title
            body (list): list of messages for body text
            instructions (list): list of game instructions to be displayed
        '''

        self.open_music = pygame.mixer.music.load('audio/Battle-Conflict.mp3')
        pygame.mixer.music.play(-1)
        self.color = (255,255,255)
        self.fonts = [pygame.font.SysFont('comicsans',100,1), pygame.font.SysFont('comicsans',30,1)]
        self.titles = ['Interstellar', 'Escort']
        self.title_location = self.display.height * (1//10)
        self.body = ["You are mankind's last hope!", 'Protect the Mothership at all costs', 'as it makes its way across the galaxy.',
                    'Beware of asteroid clusters!']
        self.instructions = ['Press any key to begin', 'Use right and left arrow keys to move.']

        while self.opening_scene == True:                           # while opening scene is True display text and background
            self.display.window.blit(Boundary.back_ground, (0,0))   # display background
            self.title_text = self.fonts[0].render(self.titles[0], 1, self.color)
            self.title_text2 = self.fonts[0].render(self.titles[1], 1, self.color)
            
            self.display.window.blit(self.title_text, ((self.display.width//2) - (self.title_text.get_width()//2), 70))
            self.display.window.blit(self.title_text2, ((self.display.width//2) - (self.title_text2.get_width()//2), 130))
            
            self.body_location = 300                                # established in loop so it is reset each time
            for body_text in self.body:
                b_t = self.fonts[1].render(body_text, 1, self.color)

                self.display.window.blit(b_t, ((self.display.width//2) - (b_t.get_width()//2), self.body_location))

                self.body_location += 30                            # move body text down 30 at a time
            
            self.instructions_location = 600                        # established in loop so it is reset each time
            for instruction in self.instructions:
                instructions_text = self.fonts[1].render(instruction, 1, self.color)
                self.display.window.blit(instructions_text, ((self.display.width//2) - (instructions_text.get_width()//2), 
                                        self.instructions_location))

                self.instructions_location += 30

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:                      # game will start upon release of any key
                    self.opening_scene = False                      # kick back out to main loop 

                if event.type == pygame.QUIT:
                    self.opening_scene = False
                    self.quit = True
                    pygame.quit()

    def end_game(self):
        '''Create Credits object and restart game upon user input

        Attributes
            end_music (pygame music): music played at game over screen
            game_over (Credits obj): credits object with the current final score
            displaying_credits (bool): control for end game loop
        '''
        pygame.mixer.music.stop()
        self.end_music = pygame.mixer.music.load('audio/Battle-Conflict.mp3')
        pygame.mixer.music.play(-1)
        self.game_over = Credits(self.score.score)                  # create credits obj
        self.game_over.write_highscores()
        self.displaying_credits = True
        
        while self.displaying_credits:
            #if self.displaying_credits == False:
            #    break
            self.display.window.blit(Boundary.back_ground, (0,0))   # display background to screen
            self.game_over.display_credits(self.display.window)     # print credits to screen
            pygame.display.update()

            pygame.time.delay(2000)                                 # delay pygame so key pressing at end of game doesn't auto restart

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:                      # reset game upon pressing and release of key
                    # Reset all object class attribute list to empty for new game
                    Asteroid.asteroid_lst[:] = []
                    ShooterObject.shots_queue[:] = []
                    Explosion.explosion_lst[:] = []
                    Health_PowerUp.current_powerups[:] = []
                    
                    # using initial game setup commands to reset everything upon restart.
                    self.music = pygame.mixer.music.load('audio/Battle-SilverMoon.mp3')
                    pygame.mixer.music.play(-1)                                 
                    self.clock = pygame.time.Clock()
                    self.run = True
                    self.display = Boundary(500, 700)                           
                    self.main_sprite = Character()                         
                    self.mothership = Mothership()
                    self.score = Score()
                    self.count = 0                                              
                    self.center_frame = 0
                    self.left_right_frame = 0
                    self.next_frame = time.time()
                    self.most_recent_key = None
                    self.powerup_timer = 0                                                              
                    self.displaying_credits = False

                if event.type == pygame.QUIT:
                    self.displaying_credits = False
                    pygame.quit()
                    #break

    def handle_key_presses(self):
        '''Move character right and left, setting character movement states and correct frames to be displayed'''
        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_LEFT]:                                 # left arrow key to move left
            self.main_sprite.move_left(self.display)            # using display as input to set boundaries for movement.
            if self.main_sprite.left == False:                  # only allowing access to branch if False so it won't run while holding down key
                self.main_sprite.left = True                    # sprite is now moving left
                self.main_sprite.right = False                  # right and center are now both False
                self.main_sprite.center = False                      
                self.left_right_frame = 0                       # resetting left&right frame count. Will help display intermediate strafe states
                self.most_recent_key = 'l'                      # setting left so intermediate strafe images used to level out spaceship

        elif keys[pygame.K_RIGHT]:                              # right arrow key to move right
            self.main_sprite.move_right(self.display)           # using display as input to set boundaries for movement.
            if self.main_sprite.right == False:                 # only allowing access to branch if False so it won't run while holding down key
                self.main_sprite.right = True
                self.main_sprite.left = False
                self.main_sprite.center = False
                self.left_right_frame = 0
                self.most_recent_key = 'r'                      # setting right so intermediate strafe images used to level out spaceship

        else:
            if self.main_sprite.center == False:                # once right or left keys are let go, if statement will run
                self.main_sprite.center = True
                self.main_sprite.right = False
                self.main_sprite.left = False
                self.left_right_frame = 0                       # resetting upon return to center will allow us to access intermediate strafe states

    def generate_shots(self):
        '''Generate shots fired from spaceship at a constant rate'''
        if (self.count % ShooterObject.shot_rate == 0):         # every 50 loops the spaceship will generate a ShooterObject(bullet)
            self.main_sprite.shoot('normal')                    # normal indicates the bullet type and specifies its properties upon creation.

    def generate_asteroids(self):
        '''Generate asteroids at a random rate'''
        # calling asteroid random number generator if numbers are the same then asteroid is generated and placed on screen
        if Asteroid.ast_diff_setting[Asteroid.current_setting] == random.randint(0,Asteroid.ast_diff_setting[Asteroid.current_setting]):
            self.a = Asteroid()

    def generate_powerup(self):
        '''Generate health and timed power ups at discrete intervals and game conditions'''
        if self.count > self.powerup_health_timer:          # health has its own timer and now is completely unlinked to other powerup generation
            if self.mothership.health_amt != 1000:          # only if the mothership has taken on some damage should powerups begin to generate
                # powerup generation is a function of game health with a max generation rate of 300
                if self.mothership.health_amt*2 == random.randint(0,self.mothership.health_amt*2 + 300): 
                    self.p = Health_PowerUp()
                    self.powerup_health_timer = self.count + 500 # cooldown timer for power ups are set at ~8 seconds
        
        if self.count > self.powerup_timer:             # power up cooldown has expired 
            if TimedPowerUp.activated == False:         # only allow power up generation if a powerup isn't in current use.
                if self.mothership.health_amt >= 500:   # havin' a good time then you should get a double XP
                    if 1000 == random.randint(0,1000):
                        TimedPowerUp('Double XP')
                        self.powerup_timer = self.count + 500 # setting cooldown for powerups ~8 seconds
                
                if self.mothership.health_amt <= 500:   # about t' die might need Insta-Kill
                    if 1000 == random.randint(0,1000):
                        TimedPowerUp('Insta-Kill')      
                        self.powerup_timer = self.count + 500

    def handle_collisions(self):
        '''Loop through all object types on screen and determine if collisions have occurred'''
        for powerup in Health_PowerUp.current_powerups:
            if (powerup.x > self.main_sprite.x) and (powerup.x < self.main_sprite.x + self.main_sprite.width)\
                 and (powerup.y + powerup.height > self.main_sprite.y)\
                      and (powerup.y + powerup.height < self.main_sprite.y + self.main_sprite.height): # within boundaries of main sprite
                if powerup.activated == False:                          # set so power up can only give mothership health once.
                    self.mothership.health_amt += powerup.health_add    # increment mothership's health
                    self.mothership.update_damage()                     # update motherships damage
                    powerup.activated = True                            # activate powerup
            if powerup.activated == True:
                if powerup.powerup_display_timer > 25:                  # turn off powerup activate after counter has reached 25
                    powerup.activated = False 
                    Health_PowerUp.current_powerups.pop(Health_PowerUp.current_powerups.index(powerup))
                    del powerup                                         # remove powerup from instance list and delete

        for t_powerup in TimedPowerUp.current_powerups:
            if (t_powerup.x > self.main_sprite.x) and (t_powerup.x < self.main_sprite.x + self.main_sprite.width)\
                    and (t_powerup.y + t_powerup.height > self.main_sprite.y)\
                         and (t_powerup.y + t_powerup.height < self.main_sprite.y + self.main_sprite.height): #within boundaries
                if TimedPowerUp.activated == False:                     # only turn switch if False, this keeps actions from repeating
                    TimedPowerUp.activated = True
                    t_powerup.effect_timer = self.count                 # setting powerup timer to current game loop number
            if TimedPowerUp.activated == True:
                if self.count - t_powerup.effect_timer > t_powerup.powerup_duration: # ~10 seconds worth of powerup
                    TimedPowerUp.activated = False                      # undos all effects from activation
                    TimedPowerUp.current_powerups.pop(TimedPowerUp.current_powerups.index(t_powerup))
                    del t_powerup                                       # remove of instance list and delete 
        
        for bullet in ShooterObject.shots_queue:
            for asteroid in Asteroid.asteroid_lst:
                if (bullet.start_x >= asteroid.x) and (bullet.start_x <= asteroid.x + asteroid.width)\
                         and (bullet.end_y <= asteroid.y + asteroid.width): # check to see if bullet is within asteroid hit box
                    # if within hit box, then more complex calculation to see if bullet is within radius is performed.
                    if ((bullet.end_y - (asteroid.y + (asteroid.width/2)))**2 + (bullet.start_x - (asteroid.x + (asteroid.width/2)))**2)**0.5 < (asteroid.width/2):
                        bullet.hit = True                                   # register hit and reduce asteroid health
                        if (TimedPowerUp.activated == True) and (TimedPowerUp.current_option == 'Insta-Kill'): # powerup effect
                            asteroid.health_amt = 0                         # instantly reduct asteroid health to zero.
                            asteroid.damage_taken += bullet.damage
                        else:
                            asteroid.health_amt -= bullet.damage            # if no powerup then just reduce ast health by bullet damage
                            asteroid.damage_taken += bullet.damage
                        asteroid.update_health_bars()

                if (asteroid.health_amt <= 0) or (asteroid.y + asteroid.width > 650):   # check deletion conditions
                    if asteroid.health_amt <= 0:                        
                        if (TimedPowerUp.activated == True) and (TimedPowerUp.current_option == 'Double XP'): # powerup effect
                            self.score.score += (asteroid.width * 2)                    # double the amount of XP you receive
                        else:
                            self.score.score += asteroid.width                          # increment score asteroid width amt
                        asteroid.destruction_method = 'negative health'                 # method informs that xp gain should be shown on screen
                    elif (asteroid.y + asteroid.width > 650):                           # has made contact with mothership
                        asteroid.destruction_method = 'off screen'
                        self.mothership.health_amt -= asteroid.damage                   # update mothership health and damage
                        self.mothership.damage_taken += asteroid.damage
                        self.mothership.update_damage() 
                        
                    Asteroid.asteroid_lst.pop(Asteroid.asteroid_lst.index(asteroid))
                    asteroid.generate_explosion()                                       # generate asteroid before deleting obj
                    del asteroid 
            
            if (bullet.hit == True) or (bullet.start_y < 0):                            # check delete conditions
                ShooterObject.shots_queue.pop(ShooterObject.shots_queue.index(bullet))
                del bullet

    def redraw_window(self):
        '''Redraw all objects onto screen'''
        self.display.window.blit(Boundary.back_ground, (0,0))                           # redrawing background.
        pygame.draw.rect(self.display.window, (255,255,255), (475, 75, 15, 550), 2)     # empty rect for powerup display
        self.mothership.draw(self.display.window)                                       # draw mothership
        self.score.draw_score(self.display.window)                                      # draw score
        self.main_sprite.draw(self.left_right_frame, self.center_frame,
                             self.most_recent_key, self.display.window)                 # draw sprite
        
        # below progresses and draws asteroids/shooting objects
        for shot in ShooterObject.shots_queue:          # accessing every ShooterObject currently in creation (stored in current_shoots)      
            shot.progress()                             # progressing each shot down the screen
            shot.draw_line(self.display.window)         # drawing shot in new location

        for ast in Asteroid.asteroid_lst:               # iterating through list of asteroids generated
            if self.count % 2 == 0:                     # move asteroids every other frame. keeps them from being too fast
                ast.progress_down()
            ast.draw_asteroid(self.display.window) 

        for powerup in Health_PowerUp.current_powerups:
            if powerup.activated == True:
                if (self.count % 5) and (powerup.powerup_display_timer < 25):   # only display every five game loop frames if its been activate
                    powerup.draw(self.display.window)
                    powerup.powerup_display_timer += 1
            else:    
                powerup.progress()                                              # if in unactivated state then have it progress down the screen
                powerup.draw(self.display.window)

        for powerup in TimedPowerUp.current_powerups:
            if TimedPowerUp.activated == True:
                if (self.count % 5) and (powerup.powerup_display_timer < 25): 
                    powerup.draw(self.display.window)
                    powerup.powerup_display_timer += 1
                if self.count - powerup.effect_timer < powerup.powerup_duration:    # if still under duration limit
                    # fill powerup bar on right of screen with yellow
                    pygame.draw.rect(self.display.window, (235, 204, 52), (475, 75, 15, 
                                    round(powerup.powerup_duration * (1 - (self.count - powerup.effect_timer)/powerup.powerup_duration))))
            else:    
                powerup.progress()                                                  # if not activated progress down screen
                powerup.draw(self.display.window)
        
        for exp in Explosion.explosion_lst:
            if self.count % 4 == 0:                                                 # switch explosion frame every four loops
                exp.current_frame += 1

            if exp.current_frame >= 11:                                             # past final frame so remove from explosion list and del object
                Explosion.explosion_lst.pop(Explosion.explosion_lst.index(exp))
                del exp
            else: 
                exp.draw(self.display.window)
    
    def __del__(self):
        '''Delete GameStart obj'''
        pass

    
if __name__ == "__main__":
    GameStart()  