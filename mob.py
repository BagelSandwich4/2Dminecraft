import pygame
from pygame.locals import *
import blocks_to_pixels
import health_bar

class Mob(pygame.sprite.Sprite):
    '''
    Class of all mobs inherited from the interactable class
    '''
    def __init__(self,image,position,size,requirement,health,health_size):
        '''
        Setting up a mob with health
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (16 pixels = 1 block)
            size - size of the .png uploaded
            requirement - None or an instance of the item class that must be held in order to interact
            health - integer represnting how much health the mob starts out with
            health_size - tuple represnting height and width of a single heart of health in pixels
        '''
        super().__init__()
        #loading the image
        img = pygame.image.load(image).convert_alpha()
        #assigning the image
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        #setting up mask
        self.mask = pygame.mask.from_surface(self.image)
        #setting it to visible
        self.visible = True
        #setting it to not passable
        self.solid = True
        #setting end to false by default
        self.end = False
        #setting position in pixels
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        #setting required instance
        self.requirement = requirement
        health_pos = [position[0], position[1]-health_size[1]]
        self.health_bar = health_bar.Health_Bar(health_pos,health_size,health)

    def damage(self,player, hotbar,drop, end=False):
        '''
        This method takes an interactable and makes the drop item visible and turns the interactable either into the newimage or invisible
        Inputs:
            player - instance of the player class
            drop - the instance of the item class that is being dropped by the interactable
            newimage - a string representing the path to the png you wish to change the interatable to. Or None if you wish the iteractable to go away
            size - a tuple representing the x and y size of the newimage in blocks
            hotbar - instance of the hotbar class
            end - boolean logic of whether or not interacting with this ends the game
        '''
        #if you are holding the right item
        correct_held_item = (self.requirement == hotbar.selected)
        #if there is health left and you are touching the mob
        if self.health_bar.hp > 0 and correct_held_item and self.mask.overlap(player.mask, [int(player.pos.x - self.pos[0]), int(player.pos.y - self.pos[1])]):
            self.health_bar.damage(1)
        #death
        if self.health_bar.hp == 0:
            self.end = end
            if drop != None:
                #setting the dropped item to visible
                drop.visible = True
            #setting the mob to invisible
            self.visible = False
            #making it no longer solid
            self.solid = False
            #getting rid of its mask
            self.mask.clear()