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

