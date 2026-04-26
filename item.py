import pygame
from pygame.locals import *
import blocks_to_pixels


class Item(pygame.sprite.Sprite):
    '''
    This class creates interactable items that the player can hold and store in their hotbar.
    '''
    def __init__(self,image,position,size,reversed=False):
        '''
        Setting up an item sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
            reversed - boolean logic showing whether or not to reverse the image
        '''
        super().__init__()
        #loading item image
        img = pygame.image.load(image).convert_alpha()
        #setting image non-reversed
        self.image_normal = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        #setting current image
        self.image = self.image_normal
        #flipping the image according to boolean logic
        if reversed == True:
            self.image = pygame.transform.flip(self.image_normal, True, False)
        #setting positional attribute
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        #setting up mask
        self.mask = pygame.mask.from_surface(self.image)
        #setting it to invisible by default
        self.visible = False
        #storing the reversed image
        self.image_reversed = pygame.transform.flip(self.image_normal, True, False)
    def pick_up(self, hotbar, player):
        '''
        This method is run if the player picks the item up. It is then stored in the players selected hotbar slot
        Inputs:
            hotbar - instance of the hotbar class
            player - instance of the player class
        '''
        # Only attempt pickup if the item is in-world and has a mask
        if not self.visible:
            return
        #if there isnt a mask make one
        if getattr(self, "mask", None) is None:
            self.mask = pygame.mask.from_surface(self.image)
        #setting up offset to check overlap
        offset = (int(player.pos.x - self.pos[0]), int(player.pos.y - self.pos[1]))
        #checking overlap
        if self.mask.overlap(player.mask, offset):
            #checking if the hotbar can take an item in the current state
            if hotbar is not None:
                accepted = hotbar.pick_up_item(self)
            if accepted:
                # hide the world item and clear its mask so it no longer collides or draws
                self.visible = False
                # clear mask so overlap won't trigger again; recreate when returning to world
                self.mask.clear()
    def holding_item(self,player):
        '''
        This determines if the item is selected and tells the view where to put the item on the player so it looks like steve is holding it.
        Inputs:
            player - instance of the player class
        '''
        if player.image == player.imageright:
            #setting hold coordinates if steve is facing right 
            self.hold_coords = self.hold_coords = [player.pos.x + 2, player.pos.y + 6]
            #setting the image to the normal image
            self.image = self.image_normal
        else:
            #setting hold coordinates if steve is facing left
            self.hold_coords = self.hold_coords = [player.pos.x - 10, player.pos.y + 6]
            #setting the image to the reversed image
            self.image = self.image_reversed

