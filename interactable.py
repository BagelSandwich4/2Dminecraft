import pygame
from pygame.locals import *
import blocks_to_pixels

class Interactable(pygame.sprite.Sprite):
    '''
    This class is for entities that are interactable like chests,mobs, and ore.
    '''
    def __init__(self,image,position,size, solid,requirement, reversed=False):
        '''
        Setting up an interactable sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
            solid - boolean logic telling whether the player can pass through the interactable
            requirement - None or an instance of the item class that must be held in order to interact
            reversed - boolean logic showing whether or not to reverse the image
        '''
        super().__init__()
        #loading the image
        img = pygame.image.load(image).convert_alpha()
        #assigning the image
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        #reversing image in neccesary
        if reversed == True:
            self.image = pygame.transform.flip(self.image, True, False)
        #setting up mask
        self.mask = pygame.mask.from_surface(self.image)
        #setting it to visible
        self.visible = True
        #setting it to not passable
        self.solid = solid
        #setting end to false by default
        self.end = False
        #setting position in pixels
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        #setting required instance
        self.requirement = requirement
    def interact(self,player,drop,newimage,size, hotbar,end=False):
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
        if self.requirement is None:
            correct_held_item = True
        else:
            correct_held_item = (self.requirement == hotbar.selected)
        if newimage != None and correct_held_item and self.mask.overlap(player.mask, [int(player.pos.x - self.pos[0]), int(player.pos.y - self.pos[1])]):
            self.end = end
            #loading the new image
            img = pygame.image.load(newimage).convert_alpha()
            #assigning the new image
            self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
            if drop != None:
                #setting the item the interactable drops to visible
                drop.visible = True
            #removing the mask so you cant interact with it again as long as it isnt the dragon
            if self.end == False:
                self.mask.clear()
        elif newimage == None and correct_held_item and self.mask.overlap(player.mask, [int(player.pos.x - self.pos[0]), int(player.pos.y - self.pos[1])]):
            self.end = end
            if drop != None:
                #setting the dropped item to visible
                drop.visible = True
            #setting the interactable to invisible
            self.visible = False
            #making it no longer solid
            self.solid = False
            #getting rid of its mask
            self.mask.clear()
    def craft(self,drop,cost,hotbar,player):
        '''
        Determines how crafting function of crafting tables works
        Inputs:
            drop - instance of the item class that is the output of the craft
            cost - instance of the item class that is required to get drop
            hotbar - instance of the hotbar class
            player - instance of the player class
        '''
        if not isinstance(cost, (list, tuple)):
            cost = [cost]
        #ensures the player is touching the crafting table
        if not self.mask.overlap(player.mask, [self.pos[0]-player.pos.x, self.pos[1]-player.pos.y]):
            return
        #checking for the item needed to craft
        if all(hotbar.check_for_item(item) for item in cost) and hotbar is not None:
            for item in cost:
                #deleting the item needed to craft
                hotbar.delete_item(item)
            #storing the crafted item in the hotbar
            hotbar.pick_up_item(drop)