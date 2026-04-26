import pygame
from pygame.locals import *
import blocks_to_pixels

vec = pygame.math.Vector2  # 2 for two dimensional

class Hotbar(pygame.sprite.Sprite):
    '''
    This is the hotbar class. It deals with the hotbar and storing the contents of it.
    '''
    def __init__(self, image, selected_image, position, size, width):
        '''
        Setting up a hotbar
        Inputs:
            image - a string representing the path to the .png file of the ui
            selected_image - a string representing the path to the .png file of the selected item ui
            position - a tuple representing the x and y coordinates of the sprite in pixels
            size - size of the .png uploaded in pixels
        '''
        super().__init__()
        #loads the image
        img = pygame.image.load(image).convert_alpha()
        s_img = pygame.image.load(selected_image).convert_alpha()
        #sets the size of the image
        self.image = pygame.transform.scale(img, (size[0], size[1]))
        self.s_image = pygame.transform.scale(s_img, (size[1],size[1]))
        #sets position of the sprite
        self.pos = [position[0],position[1]]
        #creates mask
        self.mask = pygame.mask.from_surface(self.image)
        #sets it to visible
        self.visible = True 
        #sets the hotbar to empty
        self.hotbar = [None,None,None,None,None,None,None,None,None]
        #sets initial selected slot to the first one
        self.selected_slot = 1
        self.selected = self.hotbar[0]
        #sets the positions needed to change the image of the selected slot
        self.x_positions = [width/3.3, width/3.3+ 15, width/3.3 +15*2, width/3.3 +15*3, width/3.3 +15*4, width/3.3 + 15*5, width/3.3 +15*6 , width/3.3 +15*7 , width/3.3 +15*8]
        #assigns attribute to the the selected slots position
        self.selected_coordinates = [self.x_positions[0], self.pos[1]]
    
    def change_selected(self,new_selected):
        '''
        This determines which slot is selected and changes certain varibles based on that
        '''
        self.selected_slot = new_selected
        #changes position of selected slot
        self.selected_coordinates = [self.x_positions[self.selected_slot -1], self.pos[1]]
        self.selected = self.hotbar[self.selected_slot-1]
    def pick_up_item(self,item):
        '''
        This adds an item into the selected hotbar slot. 
        Inputs:
            item - an instance of the item class to be picked up
        Returns:
            True - boolean logic that says if the item was picked up
            False - True - boolean logic that says if the item was not picked up
        '''
        #sets index of current selected slot
        i = self.selected_slot - 1
        #checks that the slot is empty
        if self.hotbar[i] is None:
            #sets the slot to the item
            self.hotbar[i] = item
            self.selected = self.hotbar[i]
            return True
        return False
    def delete_item(self,item):
        '''
        Removes an item stored in the hotbar
        Inputs:
            item: instance of the item class that is being deleted
        '''
        for i in range(0,9):
            if self.hotbar[i]  == item:
                #sets the slot to empty
                self.hotbar[i] = None
                #sets the deleted items slot to the current selected slot
                self.selected = self.hotbar[i]

    def check_for_item(self,item):
        '''
        Checks the hotbar for a specifc item
        Inputs:
            item: instance of the item class that is being searched for
        Returns:
            True: Boolean logic if the item is being stored in the hotbar
            False: Boolean logic if the item is not being stored in the hotbar
        '''
        for i in range(0,9):
            if self.hotbar[i] == item:
                return True
        return False