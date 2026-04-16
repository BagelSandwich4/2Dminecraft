import pygame
import sys
import random
import blocks_to_pixels
from pygame.locals import *
 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
#setting constants like screensize and physics stuff 
HEIGHT = 208
HEIGHT_BLOCKS = 13
WIDTH = 320
WIDTH_BLOCKS = 20
ACC = 0.5
FRIC = -0.4
FPS = 60
pygame.display.set_caption("Minecraft 2D")
pygame.mouse.set_visible(False)
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
bg_image = pygame.image.load("backgrounds\\sky.png").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self,size):
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
        self.size = [blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])]
    def change_image(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.image = self.imageleft
        if pressed_keys[K_RIGHT]:
            self.image = self.imageright
    def move(self):
        #controller
        #gravity
        self.acc = vec(0,0.5)
        #storing pressed keys
        pressed_keys = pygame.key.get_pressed()
        #tells the computer to move when keys are pressed  
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC 
        #makes friction and stuff happen
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #makes it so you cant jump off the platform
        if self.pos.x < 4: 
            self.pos.x = 4
            self.vel.x = 0
    
        if self.pos.x > WIDTH - 4:
            self.pos.x = WIDTH - 4
            self.vel.x = 0
        self.mask.set_at((0,0), 1)
        self.mask.set_at((self.surf.get_width()-1, self.surf.get_height()-1), 1)
    def update(self):
        #makes it so you dont fall through the floor
        for plat in platforms:
            if self.mask.overlap(plat.mask, [plat.pos[0]-self.pos.x, plat.pos[1]-self.pos.y]):
                self.vel.y = 0
                self.pos.y = plat.pos[1] - self.image.get_height()
        '''
        for temp_interactable in interactables:
            if self.mask.overlap(temp_interactable.mask, [temp_interactable.pos[0]-self.pos.x, temp_interactable.pos[1]-self.pos.y]):
                self.vel.y = 0
        '''
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
        for temp_platform in platforms:
            if self.mask.overlap(temp_platform.mask, [temp_platform.pos[0]-self.pos.x, temp_platform.pos[1]-self.pos.y]):
                self.vel.y = -8.5
 
class build(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        #size
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        #position
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        self.mask = pygame.mask.from_surface(self.image)
        self.visible = True

class platform(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        self.size = [blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])]
        self.visible = True

class item(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        self.mask = pygame.mask.from_surface(self.image)
        self.visible = False
    def pick_up(self):
        for temp_item in items:
            if self.mask.overlap(P1.mask, [temp_item.pos[0]-P1.pos.x, temp_item.pos[1]-P1.pos.y]):
                self.visible = False
                
        
class interactable(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        '''
        Setting up an interactable sprite
        Inputs:
            image - a string representing the path to the .png file
            position - 
        '''
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        self.mask = pygame.mask.from_surface(self.image)
        self.visible = True
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
    def interact(self,drop,newimage,size):
        if self.mask.overlap(P1.mask, [self.pos[0]-P1.pos.x, self.pos[1]-P1.pos.y]):
            img = pygame.image.load(newimage).convert_alpha()
            self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
            drop.visible = True

#placement of entities
VILLAGEHOUSE = build("other_sprites\\Village House.png",(10,5),(7,7))
GRASS = platform("platforms\\platform_grass.png",(0,12),(WIDTH_BLOCKS, 1))
CAVE_ENTRANCE = platform("platforms\\platform_cave_entrance.png",(20,3),(10,13))
P1 = Player((1,2))
CHEST = interactable("other_sprites\\chest_front.png",(17,11),(1,1))
IRON_PICKAXE = item("other_sprites\\iron_pickaxe.png",(18,11),(1,1))

#creating sprite groups
builds = pygame.sprite.Group()
platforms = pygame.sprite.Group()
interactables = pygame.sprite.Group()
items = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#adding them to the groups
builds.add(VILLAGEHOUSE)
platforms.add(GRASS)
platforms.add(CAVE_ENTRANCE)
interactables.add(CHEST)
all_sprites.add(VILLAGEHOUSE)
all_sprites.add(GRASS)
all_sprites.add(P1)
all_sprites.add(CHEST)
all_sprites.add(IRON_PICKAXE)
all_sprites.add(CAVE_ENTRANCE)

while True:
    #main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
    #scrolling of screen
    scroll_x = P1.pos.x - (WIDTH / 2)
    displaysurface.blit(bg_image, (0, 0)) 
    #draws all the sprites
    for entity in all_sprites:
        if entity.visible:
            draw_pos = (entity.pos[0] - scroll_x, entity.pos[1])
            displaysurface.blit(entity.image, draw_pos)
        
    #every tick it checks these
    P1.move()
    P1.update()
    P1.change_image()
    IRON_PICKAXE.pick_up()
    CHEST.interact(IRON_PICKAXE,"other_sprites\\chest_front.png",(1,1))
    pygame.display.update()
    FramePerSec.tick(FPS)
