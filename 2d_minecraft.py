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
        '''
        Setting up the players sprite
        Inputs:
            size - size of the .png uploaded
        '''
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
        self.hotbar = ["","","","","","","","",""] #21 180
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
        number_keys = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
        #tells the computer to move when keys are pressed  
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        #checks if they move which slot is selected
        for key, i in zip(number_keys, range(1,9)):
            if pressed_keys[key]:
                HOTBAR.change_selected(i)
        #makes friction and stuff happen
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #makes it so you cant jump off the platform
        '''
        if self.pos.x < 4: 
            self.pos.x = 4
            self.vel.x = 0
    
        if self.pos.x > WIDTH - 4:
            self.pos.x = WIDTH - 4
            self.vel.x = 0
        '''
        self.mask.set_at((0,0), 1)
        self.mask.set_at((self.surf.get_width()-1, self.surf.get_height()-1), 1)
    
    def update(self):
        #makes it so you dont fall through the floor
        for plat in platforms:
            if self.vel.y > 0:
                # 1. Calculate offset to check if we are touching the platform at all
                offset_x = int(plat.pos[0] - self.pos.x)
                offset_y = int(plat.pos[1] - self.pos.y)
                
                if self.mask.overlap(plat.mask, (offset_x, offset_y)):
                    
                    # 2. Find the EXACT pixel coordinate on the platform we hit
                    plat_offset_x = int(self.pos.x - plat.pos[0])
                    plat_offset_y = int(self.pos.y - plat.pos[1])
                    plat_hit = plat.mask.overlap(self.mask, (plat_offset_x, plat_offset_y))
                    
                    if plat_hit:
                        # plat_hit[1] is the local Y coordinate on the platform.
                        # Add plat.pos[1] to get the absolute world Y coordinate of the floor.
                        floor_y = plat.pos[1] + plat_hit[1]
                        
                        # 3. Only snap if the floor is below the upper section of the player.
                        # This prevents the player from instantly climbing a vertical wall
                        # when walking into it, but allows them to walk on lower floors inside a large image!
                        if floor_y > self.pos.y + (self.image.get_height() * 0.25):
                            self.pos.y = floor_y - self.image.get_height()
                            self.vel.y = 0
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
        pressed_keys = pygame.key.get_pressed()
        for temp_platform in platforms:
            if self.mask.overlap(temp_platform.mask, [temp_platform.pos[0]-self.pos.x, temp_platform.pos[1]-self.pos.y-1]) and pressed_keys[K_SPACE]:
                self.vel.y = -8.5

class hotbar(pygame.sprite.Sprite):
    def __init__(self, image, selected_image, position, size):
        '''
        Setting up a hotbar
        Inputs:
            image - a string representing the path to the .png file of the ui
            selected_image - a string representing the path to the .png file of the selected item ui
            position - a tuple representing the x and y coordinates of the sprite in pixels
            size - size of the .png uploaded in pixels
        '''
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        s_img = pygame.image.load(selected_image).convert_alpha()
        #size
        self.image = pygame.transform.scale(img, (size[0], size[1]))
        self.s_image = pygame.transform.scale(s_img, (size[1],size[1]))
        #position
        #position
        self.pos = [position[0],position[1]]
        self.mask = pygame.mask.from_surface(self.image)
        self.visible = True 
        self.selected = 1
        self.hotbar = [IRON_PICKAXE,None,None,None,None,IRON_PICKAXE,None,None,None]
        self.x_positions = [WIDTH/3.3, WIDTH/3.3+ 15, WIDTH/3.3 +15*2, WIDTH/3.3 +15*3, WIDTH/3.3 +15*4 , WIDTH/3.3 +15*6 , WIDTH/3.3 +15*7 , WIDTH/3.3 +15*8]
        self.selected_coordinates = [self.x_positions[0], self.pos[1]]
    def change_selected(self,new_selected):
        self.selected_slot = new_selected
        self.selected_coordinates = [self.x_positions[self.selected_slot -1], self.pos[1]]
        self.selected = self.hotbar[self.selected_slot-1]
    def pick_up_item(self,item):
        if self.selected == None:
            self.hotbar[self.selected_slot-1] = item
        
 
class build(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        '''
        Setting up an building sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
        '''
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
        '''
        Setting up an platform sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
        '''
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        self.size = [blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])]
        self.visible = True

class item(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        '''
        Setting up an item sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
        '''
        super().__init__()
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        self.mask = pygame.mask.from_surface(self.image)
        self.visible = False
    def pick_up(self):
        for temp_item in items:
            if self.mask.overlap(P1.mask, [temp_item.pos[0]-P1.pos.x, temp_item.pos[1]-P1.pos.y]):
                HOTBAR.pick_up_item(temp_item)
                self.visible = False
                
        
class interactable(pygame.sprite.Sprite):
    def __init__(self,image,position,size):
        '''
        Setting up an interactable sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
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


#placement of entities
VILLAGEHOUSE = build("other_sprites\\Village House.png",(10,5),(7,7))
MOUNTAIN = build("backgrounds\\background_cave_entrance.png", (15,0),(20,13))
GRASS = platform("platforms\\platform_grass.png",(0,12),(WIDTH_BLOCKS, 1))
CAVE_ENTRANCE = platform("platforms\\platform_cave_entrance.png",(20,3),(10,13))
CAVE_CONT = platform("platforms\\platform_cave_entrance.png",(27,6),(10,13))
P1 = Player((1,2))
CHEST = interactable("other_sprites\\chest_front.png",(17,11),(1,1))
IRON_PICKAXE = item("items\\iron_pickaxe.png",(18,11),(1,1))
DIAMOND = item("items\\diamond.png",(20,11),(1,1))
HOTBAR = hotbar("other_sprites\\hotbar.png", "other_sprites\\selected_hotbar_slot.png", (WIDTH/3.3, HEIGHT-15), [135,16])
#real size 180x21

#creating sprite groups
builds = pygame.sprite.Group()
platforms = pygame.sprite.Group()
interactables = pygame.sprite.Group()
items = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_ui = pygame.sprite.Group()

#adding them to the groups
builds.add(VILLAGEHOUSE)
builds.add(MOUNTAIN)
platforms.add(GRASS)
platforms.add(CAVE_ENTRANCE)
platforms.add(CAVE_CONT)
interactables.add(CHEST)
items.add(DIAMOND)
items.add(IRON_PICKAXE)
all_sprites.add(VILLAGEHOUSE)
all_sprites.add(GRASS)
all_sprites.add(MOUNTAIN)
all_sprites.add(P1)
all_sprites.add(CHEST)
all_sprites.add(IRON_PICKAXE)
all_sprites.add(CAVE_CONT)
all_sprites.add(CAVE_ENTRANCE)
all_sprites.add(DIAMOND)
all_ui.add(HOTBAR)

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
    scroll_y = 0
    if P1.pos.y > blocks_to_pixels.blocks_to_pixels(12):
        scroll_y = P1.pos.y - (HEIGHT/2)
    displaysurface.blit(bg_image, (0, 0)) 
    #draws all the sprites
    for entity in all_sprites:
        if entity.visible:
            draw_pos = (entity.pos[0] - scroll_x, entity.pos[1] - scroll_y)
            displaysurface.blit(entity.image, draw_pos)
    
    #ensures hotbar stays in the same place while moving
    draw_pos = (HOTBAR.pos[0], HOTBAR.pos[1])
    displaysurface.blit(HOTBAR.image, draw_pos)
    #drawing selected hotbar slot
    displaysurface.blit(HOTBAR.s_image, HOTBAR.selected_coordinates)
    #placing items
    for i in range(9):
        slot = HOTBAR.hotbar[i]
        if slot != None:
            draw_pos = [HOTBAR.x_positions[i], HOTBAR.pos[1]]
            displaysurface.blit(slot.image, draw_pos)
        if i+1 == HOTBAR.selected_slot:
            draw_pos = P1.pos
            displaysurface.blit(slot.image, draw_pos)
    
    #code for displaying masks just change the sprite and it will display in red
    #display_mask(DIAMOND)

    #every tick it checks these
    P1.move()
    P1.update()
    P1.change_image()
    IRON_PICKAXE.pick_up()
    CHEST.interact(IRON_PICKAXE,"other_sprites\\chest_front.png",(1,1))
    pygame.display.update()
    FramePerSec.tick(FPS)

'''
    for sprite in all_sprites:
        if hasattr(sprite, "mask"):
            mask_surface = sprite.mask.to_surface(setcolor=(255,0,0), unsetcolor=(0,0,0,0))
            draw_pos = (sprite.pos[0] - scroll_x, sprite.pos[1])
            displaysurface.blit(mask_surface, draw_pos)
'''