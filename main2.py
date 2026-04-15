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

FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
bg_image = pygame.image.load("sky.png").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self,size):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        steve_right = pygame.image.load("Steve_Right.png").convert_alpha()
        self.imageright = pygame.transform.scale(steve_right, (8,31))
        self.image = self.imageright
        steve_left = pygame.image.load("Steve_Left.png").convert_alpha()
        self.imageleft = pygame.transform.scale(steve_left, (8,31))
        self.rect = self.image.get_rect()
        self.pos = vec((75, 80))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.visible = True
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
        self.rect.midbottom = self.pos
    def update(self):
        #makes it so you dont fall through the floor
        hits = pygame.sprite.spritecollide(P1 , platforms, False)
        interactable_hits = pygame.sprite.spritecollide(P1, interactables, False)
        if P1.vel.y > 0 and hits:
            self.vel.y = 0
            self.pos.y = hits[0].rect.top + 1
        """
        if interactable_hits:
            for chest in interactable_hits:
                if self.vel.x > 0:
                    self.pos.x = chest.rect.left - (self.rect.width / 2)
                elif self.vel.x < 0:
                    self.pos.x = chest.rect.right + (self.rect.width / 2)
                
                self.vel.x = 0
                self.rect.midbottom = self.pos
        """

        
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -8.5
 
class build(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        #size
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        #position
        self.rect = self.image.get_rect(bottomleft = (blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])))
        self.visible = True

class platform(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        self.rect = self.image.get_rect(midbottom = (blocks_to_pixels.blocks_to_pixels(position[0]), blocks_to_pixels.blocks_to_pixels(position[1])))
        self.visible = True

class item(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        self.rect = self.image.get_rect(bottomleft = (blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])))
        self.visible = False
    def pick_up(self):
        if pygame.sprite.spritecollide(P1,items,False):
            self.rect = self.image.get_rect(bottomleft = (blocks_to_pixels.blocks_to_pixels(0),blocks_to_pixels.blocks_to_pixels(0)))
        

class interactable(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        self.rect = self.image.get_rect(bottomleft = (blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])))
        self.visible = True
    def interact(self,drop,newimage,size):
        if pygame.sprite.spritecollide(P1, interactables, False):
            img = pygame.image.load(newimage).convert_alpha()
            self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
            drop.visible = True

VILLAGEHOUSE = build("Village House.png",(10,12),(7,7))
GRASS = platform("platform_grass.png",[WIDTH_BLOCKS/2,13],[WIDTH_BLOCKS, 1])
CAVE_ENTRANCE = platform("platform_cave_entrance.png",[25,13],[10,5])
P1 = Player((1,2))
CHEST = interactable("chest_front.png",(17,12),(1,1))
IRON_PICKAXE = item("iron_pickaxe.png",(18,12),(1,1))
builds = pygame.sprite.Group()
platforms = pygame.sprite.Group()
interactables = pygame.sprite.Group()
items = pygame.sprite.Group()
builds.add(VILLAGEHOUSE)
platforms.add(GRASS)
platforms.add(CAVE_ENTRANCE)
interactables.add(CHEST)

all_sprites = pygame.sprite.Group()
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
            draw_pos = (entity.rect.x - scroll_x, entity.rect.y)
            displaysurface.blit(entity.image, draw_pos)
        
    #every tick it checks these
    P1.move()
    P1.update()
    P1.change_image()
    IRON_PICKAXE.pick_up()
    CHEST.interact(IRON_PICKAXE,"chest_front.png",(1,1))
    pygame.display.update()
    FramePerSec.tick(FPS)
