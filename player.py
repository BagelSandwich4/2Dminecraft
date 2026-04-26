import pygame
import sys
import random
import blocks_to_pixels
from pygame.locals import *

vec = pygame.math.Vector2  # 2 for two dimensional
#setting acceleration of the player as it moves
ACC = 0.8
#setting friction of the player as it moves
FRIC = -0.4
#setting frames per second
FPS = 60

class Player(pygame.sprite.Sprite):
    '''
    Class that determines everything to do with the player.
    '''
    def __init__(self,size):
        '''
        Setting up the players sprite
        Inputs:
            size - size of the .png uploaded
        '''
        super().__init__() 
        self.surf = pygame.Surface((8, 31))
        self.surf.fill((128,255,40))
        steve_right = pygame.image.load("sprites\\player sprites\\Steve_Right.png").convert_alpha()
        self.imageright = pygame.transform.scale(steve_right, (8,31))
        self.image = self.imageright
        #loading steves left side image
        steve_left = pygame.image.load("sprites\\player sprites\\Steve_Left.png").convert_alpha()
        self.imageleft = pygame.transform.scale(steve_left, (8,31))
        #creating steves mask which determines whether he is overlapping other sprites
        self.mask = pygame.mask.from_surface(self.image)
        #setting the players initial position
        self.pos = vec(75, 80)
        #setting the players initial velocity
        self.vel = vec(0,0)
        #setting the players initial acceleration
        self.acc = vec(0,0)
        #setting the players to visible
        self.visible = True
        #determining whether steve is touching a platform
        try:
            self.grounded = self.grounded
        except AttributeError:
            self.grounded = False
        #setting size as an attribute
        self.size = [blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])]

    def change_image(self):
        '''
        Changes the image of steve from left to right view when moving left or right.
        '''
        #showing which keys are pressed
        pressed_keys = pygame.key.get_pressed()
        #changing image if he is going left
        if pressed_keys[K_LEFT]:
            self.image = self.imageleft
        #changing image if he is going right
        if pressed_keys[K_RIGHT]:
            self.image = self.imageright

    def move(self, hotbar):
        '''
        This is the controller. It tells the model what to do when someone presses a key and controlls physics of the player
        '''
        #controller
        #constantly setting gravity as acceleration downwards
        if not self.grounded:
            self.acc = vec(0,.5)
        else:
            self.acc = vec(0,0)
        #storing pressed keys
        pressed_keys = pygame.key.get_pressed()
        #storing the number keys pressed for use in the hotbar
        number_keys = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
        #tells the computer to move left and right when keys are pressed
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        #checks if they press one of the numbers selected and telling the HOTBAR instance which one has been selected
        for key, i in zip(number_keys, range(1,10)):
            if pressed_keys[key]:
                hotbar.change_selected(i)
        #setting acceleration velocity and position using current and set values
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #setting steves mask to be at the same position as the image of steve
        self.mask.set_at((0,0), 1)
        self.mask.set_at((self.surf.get_width()-1, self.surf.get_height()-1), 1)
    
    def update(self, platforms, interactables, solid_mask):
        '''
        This is the update method. It makes it so the player doesnt fall through the floor or pass through entities.
        '''
        #sets the player to be touching the ground by default
        self.grounded = False
        #makes it so you dont fall through the floor by setting every platform to be solid
        for plat in platforms:
            solid_mask(plat, self)
        #makes it so you cant pass through the solid interacables 
        for temp_interactable in interactables:
            if temp_interactable.solid == True:
                solid_mask(temp_interactable,self)

    def jump(self, platforms):
        '''
        This makes the player jump.
        '''
        #reads which keys are pressed
        pressed_keys = pygame.key.get_pressed()
        #ensures that the player is touching the platorm to start
        for temp_platform in platforms:
            if self.mask.overlap(temp_platform.mask, [temp_platform.pos[0]-self.pos.x, temp_platform.pos[1]-self.pos.y-1]) and pressed_keys[K_SPACE]:
                #sets velocity upward
                self.vel.y = -7.5
    def freeze(self):
        '''
        This prevents the player from moving.
        '''
        pygame.event.set_blocked([pygame.KEYDOWN, pygame.KEYUP])


