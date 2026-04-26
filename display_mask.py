import pygame
import sys
import random
import blocks_to_pixels
from pygame.locals import *
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
HEIGHT = 208
HEIGHT_BLOCKS = 13
WIDTH = 320
WIDTH_BLOCKS = 20
scroll_x = int(P1.pos.x - (WIDTH / 2))
scroll_y = 0

def display_mask(sprite):
    '''
    Displays the mask of a given sprite for debugging
    Inputs:
        sprite - a class instance of any sprite
    '''
    sprite.visible = False
    mask_surface = sprite.mask.to_surface(setcolor=(255, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
    draw_pos = (sprite.pos[0] - scroll_x, sprite.pos[1])
    displaysurface.blit(mask_surface, draw_pos)