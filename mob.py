"""
Contains Mob class
"""
import pygame
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
            position - a tuple representing the x and y
            coordinates of the sprite in blocks (16 pixels = 1 block)
            size - size of the .png uploaded
            requirement - None or an instance of the item
            class that must be held in order to interact
            health - integer represnting how much health
            the mob starts out with
            health_size - tuple represnting height and width
            of a single heart of health in pixels
        '''
        super().__init__()
        #loading the image
        img = pygame.image.load(image).convert_alpha()
        #assigning the image
        self.image = pygame.transform.scale(img,
                (blocks_to_pixels.blocks_to_pixels(size[0]),
                blocks_to_pixels.blocks_to_pixels(size[1])))
        #setting up mask
        self.mask = pygame.mask.from_surface(self.image)
        #setting it to visible
        self.visible = True
        #setting it to not passable
        self.solid = True
        #setting end to false by default
        self.end = False
        #setting position in pixels
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),
                    blocks_to_pixels.blocks_to_pixels(position[1])]
        #setting required instance
        self.requirement = requirement
        health_pos = [self.pos[0], self.pos[1]-health_size[1]]
        self.health_bar = health_bar.HealthBar(health_pos,health)
        self.life = True

    def damage(self,player, hotbar,drop, cursor_pos,click, end=False):
        '''
        This method takes an interactable and makes the drop item visible
          and turns the interactable either into the newimage or invisible
        Inputs:
            player - instance of the player class
            drop - the instance of the item
            class that is being dropped by the interactable
            newimage - a string representing the path to the png
            you wish to change the interatable to.
            Or None if you wish the iteractable to go away
            size - a tuple representing the
            x and y size of the newimage in blocks
            hotbar - instance of the hotbar class
            cursor_pos - a tuple containing the position of the cursor in pixels
            click - tuple with boolean logic saying whether the player hit left click old,new
            end - boolean logic of whether or not
            interacting with this ends the game
        '''
        #if you are holding the right item
        correct_held_item = self.requirement == hotbar.selected
        #ensuring you're cursor is over the mob
        pos_in_mask = cursor_pos[0] - self.pos[0], cursor_pos[1] - self.pos[1]
        mask_w, mask_h = self.mask.get_size()
        touching = False
        if 0 <= pos_in_mask[0] < mask_w and 0 <= pos_in_mask[1] < mask_h:
            touching = bool(self.mask.get_at(pos_in_mask))
        #boolean logic so the first click is the only one that deals damage
        first_click = (click[1] and not click[0])
        #if there is health left and you are touching the mob and holding the correct item
        if (self.health_bar.hp > 0 and correct_held_item
            and touching and first_click):
            self.health_bar.damage(1)
        #death
        if self.health_bar.hp == 0 and self.life is True:
            self.end = end
            if drop is not None and drop.visible is False:
                #setting the dropped item to visible
                drop.visible = True
                drop.mask = pygame.mask.from_surface(drop.image)
            #setting the mob to invisible
            self.visible = False
            #making it no longer solid
            self.solid = False
            #getting rid of its mask
            self.mask.clear()
            self.life = False
