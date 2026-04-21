import pygame
import sys
import random
import blocks_to_pixels
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self,size):
        '''
        Setting up the players sprite
        Inputs:
            size - size of the .png uploaded
        '''
        super().__init__() 
        self.surf = pygame.Surface((8, 31))
        self.surf.fill((128,255,40))
        steve_right = pygame.image.load("player\\Steve_Right.png").convert_alpha()
        self.imageright = pygame.transform.scale(steve_right, (8,31))
        self.image = self.imageright
        steve_left = pygame.image.load("player\\Steve_Left.png").convert_alpha()
        self.imageleft = pygame.transform.scale(steve_left, (8,31))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = vec(75, 80)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.visible = True
        try:
            self.grounded = self.grounded
        except AttributeError:
            self.grounded = False

        self.size = [blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])]

    def change_image(self):
        '''
        Changes the image of steve from left to right view when moving left or right.
        '''
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.image = self.imageleft
        if pressed_keys[K_RIGHT]:
            self.image = self.imageright

    def move(self):
        '''
        This is the controller. It tells the model what to do when someone presses a key
        '''
        #controller
        #gravity
        if not self.grounded:
            self.acc = vec(0,.5)
        else:
            self.acc = vec(0,0)
        #storing pressed keys
        pressed_keys = pygame.key.get_pressed()
        number_keys = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
        #tells the computer to move when keys are pressed  
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        #checks if they move which slot is selected
        for key, i in zip(number_keys, range(1,9)):
            if pressed_keys[key]:
                HOTBAR.change_selected(i)
        #makes friction and stuff happen
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #makes it so you cant jump off the platform
        '''
        if self.pos.x < 4: 
            self.pos.x = 4
            self.vel.x = 0
    
        if self.pos.x > WIDTH - 4:
            self.pos.x = WIDTH - 4
            self.vel.x = 0
        '''
        self.mask.set_at((0,0), 1)
        self.mask.set_at((self.surf.get_width()-1, self.surf.get_height()-1), 1)
    
    def update(self):
        '''
        This is the update method. It makes it so the player doesnt fall through the floor or pass through entities.
        '''
        self.grounded = False
        #makes it so you dont fall through the floor
        for plat in platforms:
            solid_mask(plat)
        #makes it so you cant pass through the solid interacables 
        for temp_interactable in interactables:
            if temp_interactable.solid == True:
                solid_mask(temp_interactable)
        
        """
        if interactable_hits:
            for chest in interactable_hits:
                if self.vel.x > 0:
                    self.pos.x = chest.mask.left - (self.mask.width / 2)
                elif self.vel.x < 0:
                    self.pos.x = chest.mask.right + (self.mask.width / 2)
                
                self.vel.x = 0
                self.mask.set_at((0,0), 1)
                self.mask.set_at((self.surf.get_width()-1, self.surf.get_height()-1), 1)
        """
        

        
    def jump(self):
        '''
        This makes the player jump.
        '''
        pressed_keys = pygame.key.get_pressed()
        for temp_platform in platforms:
            if self.mask.overlap(temp_platform.mask, [temp_platform.pos[0]-self.pos.x, temp_platform.pos[1]-self.pos.y-1]) and pressed_keys[K_SPACE]:
                self.vel.y = -8.5