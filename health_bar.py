import pygame
from pygame.locals import *
import blocks_to_pixels

class Health_Bar(pygame.sprite.Sprite):
    def __init__(self, position, max_hp):
        '''
        Setting up the health bar
        Inputs:
            position - tuple containing the x and y coordinates of the health bar as ints
            max_hp - integer representing the maximum health points the entity can have
        '''
        self.max_hp = max_hp
        self.hp = max_hp
        self.x_positions = [position[0]]
        self.y_position = position[1]
        self.size = (10,10)
        for _ in range(int((self.hp )/2)):
            self.x_positions.append(self.x_positions[-1] + self.size[0])
        #loading images
        full_heart_image = pygame.image.load("sprites\\health\\heart_full.png").convert_alpha()
        self.full_heart =  pygame.transform.scale(full_heart_image, self.size)
        half_heart_image = pygame.image.load("sprites\\health\\heart_full.png").convert_alpha()
        self.half_heart =  pygame.transform.scale(half_heart_image, self.size)

    def damage(self, damage_taken):
        '''
        Takes damage to the health bar
        Inputs:
            damage_taken - integer representing how many half hearts of damage were taken
        '''
        self.hp -= damage_taken
        self.x_positions = self.x_positions[0:self.hp-1]

