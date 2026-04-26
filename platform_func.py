import pygame
from pygame.locals import *
import blocks_to_pixels

class Platform(pygame.sprite.Sprite):
    '''
    This class creates the floor of the game
    '''
    def __init__(self,image,position,size, reversed=False):
        '''
        Setting up an platform sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
            reversed - boolean logic telling the class to reverse the image
        '''
        super().__init__()
        #loading the image
        img = pygame.image.load(image).convert_alpha()
        #setting up the image according to size
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        #flipping the image according to boolean reversed logic
        if reversed == True:
            self.image = pygame.transform.flip(self.image, True, False)
        #setting up mask
        self.mask = pygame.mask.from_surface(self.image)
        #setting positional attribute
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        #setting size attribute 
        self.size = [blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])]
        #setting it to visible
        self.visible = True