import pygame
from pygame.locals import *
import blocks_to_pixels

class Build(pygame.sprite.Sprite):
    '''
    This is used for creating sprites that you can pass through and are not interactable
    '''
    def __init__(self,image,position,size,reversed=False):
        '''
        Setting up an building sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
        '''
        super().__init__()
        #loads image item
        img = pygame.image.load(image).convert_alpha()
        #sets image to scale of item
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        if reversed == True:
            self.image = pygame.transform.flip(self.image, True, False)
        #sets position
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        #creates mask
        self.mask = pygame.mask.from_surface(self.image)
        #sets it to visible
        self.visible = True

