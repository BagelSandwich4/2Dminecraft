import pygame
import sys
import random
import blocks_to_pixels
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
#setting constants
#setting screensize
HEIGHT = 208
HEIGHT_BLOCKS = 13
WIDTH = 320
WIDTH_BLOCKS = 20
#setting acceleration of the player as it moves
ACC = 0.8
#setting friction of the player as it moves
FRIC = -0.4
#setting frames per second
FPS = 60
# telling pygame to set the caption to Minecraft 2D
pygame.display.set_caption("Minecraft 2D")
# telling pygame to set the mouse to invisible
pygame.mouse.set_visible(False)
# telling pygame to set the clock
FramePerSec = pygame.time.Clock()
#telling pygame we want to open a window with our set size
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
#setting the background of the game
bg_image = pygame.image.load("sprites\\backgrounds\\sky.png").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

class player(pygame.sprite.Sprite):
    '''
    Class that determines everything to do with the player.
    '''
    def __init__(self,size):
        '''
        Setting up the players sprite
        Inputs:
            size - size of the .png uploaded
        '''
        super().__init__() 
        self.surf = pygame.Surface((8, 31))
        self.surf.fill((128,255,40))
        steve_right = pygame.image.load("sprites\\player sprites\\Steve_Right.png").convert_alpha()
        self.imageright = pygame.transform.scale(steve_right, (8,31))
        self.image = self.imageright
        #loading steves left side image
        steve_left = pygame.image.load("sprites\\player sprites\\Steve_Left.png").convert_alpha()
        self.imageleft = pygame.transform.scale(steve_left, (8,31))
        #creating steves mask which determines whether he is overlapping other sprites
        self.mask = pygame.mask.from_surface(self.image)
        #setting the players initial position
        self.pos = vec(75, 80)
        #setting the players initial velocity
        self.vel = vec(0,0)
        #setting the players initial acceleration
        self.acc = vec(0,0)
        #setting the players to visible
        self.visible = True
        #determining whether steve is touching a platform
        try:
            self.grounded = self.grounded
        except AttributeError:
            self.grounded = False
        #setting size as an attribute
        self.size = [blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])]

    def change_image(self):
        '''
        Changes the image of steve from left to right view when moving left or right.
        '''
        #showing which keys are pressed
        pressed_keys = pygame.key.get_pressed()
        #changing image if he is going left
        if pressed_keys[K_LEFT]:
            self.image = self.imageleft
        #changing image if he is going right
        if pressed_keys[K_RIGHT]:
            self.image = self.imageright

    def move(self):
        '''
        This is the controller. It tells the model what to do when someone presses a key and controlls physics of the player
        '''
        #controller
        #constantly setting gravity as acceleration downwards
        if not self.grounded:
            self.acc = vec(0,.5)
        else:
            self.acc = vec(0,0)
        #storing pressed keys
        pressed_keys = pygame.key.get_pressed()
        #storing the number keys pressed for use in the hotbar
        number_keys = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
        #tells the computer to move left and right when keys are pressed
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        #checks if they press one of the numbers selected and telling the HOTBAR instance which one has been selected
        for key, i in zip(number_keys, range(1,10)):
            if pressed_keys[key]:
                HOTBAR.change_selected(i)
        #setting acceleration velocity and position using current and set values
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #setting steves mask to be at the same position as the image of steve
        self.mask.set_at((0,0), 1)
        self.mask.set_at((self.surf.get_width()-1, self.surf.get_height()-1), 1)
    
    def update(self):
        '''
        This is the update method. It makes it so the player doesnt fall through the floor or pass through entities.
        '''
        #sets the player to be touching the ground by default
        self.grounded = False
        #makes it so you dont fall through the floor by setting every platform to be solid
        for plat in platforms:
            solid_mask(plat, self)
        #makes it so you cant pass through the solid interacables 
        for temp_interactable in interactables:
            if temp_interactable.solid == True:
                solid_mask(temp_interactable,self)

    def jump(self):
        '''
        This makes the player jump.
        '''
        #reads which keys are pressed
        pressed_keys = pygame.key.get_pressed()
        #ensures that the player is touching the platorm to start
        for temp_platform in platforms:
            if self.mask.overlap(temp_platform.mask, [temp_platform.pos[0]-self.pos.x, temp_platform.pos[1]-self.pos.y-1]) and pressed_keys[K_SPACE]:
                #sets velocity upward
                self.vel.y = -7.5
    def freeze(self):
        '''
        This prevents the player from moving.
        '''
        pygame.event.set_blocked([pygame.KEYDOWN, pygame.KEYUP])

class hotbar(pygame.sprite.Sprite):
    '''
    This is the hotbar class. It deals with the hotbar and storing the contents of it.
    '''
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
        self.x_positions = [WIDTH/3.3, WIDTH/3.3+ 15, WIDTH/3.3 +15*2, WIDTH/3.3 +15*3, WIDTH/3.3 +15*4, WIDTH/3.3 + 15*5, WIDTH/3.3 +15*6 , WIDTH/3.3 +15*7 , WIDTH/3.3 +15*8]
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
        
class build(pygame.sprite.Sprite):
    '''
    This is used for creating sprites that you can pass through and are not interactable
    '''
    def __init__(self,image,position,size,reversed=False):
        '''
        Setting up an building sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
        '''
        super().__init__()
        #loads image item
        img = pygame.image.load(image).convert_alpha()
        #sets image to scale of item
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        if reversed == True:
            self.image = pygame.transform.flip(self.image, True, False)
        #sets position
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        #creates mask
        self.mask = pygame.mask.from_surface(self.image)
        #sets it to visible
        self.visible = True
class platform(pygame.sprite.Sprite):
    '''
    This class creates the floor of the game
    '''
    def __init__(self,image,position,size, reversed=False):
        '''
        Setting up an platform sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
        '''
        super().__init__()
        #loading the image
        img = pygame.image.load(image).convert_alpha()
        #setting up the image according to size
        self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
        #flipping the image according to boolean reversed logic
        if reversed == True:
            self.image = pygame.transform.flip(self.image, True, False)
        #setting up mask
        self.mask = pygame.mask.from_surface(self.image)
        #setting positional attribute
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
        #setting size attribute 
        self.size = [blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])]
        #setting it to visible
        self.visible = True

class item(pygame.sprite.Sprite):
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
        #initializing the coordinates where the image will be drawn for steve to hold it
        self.hold_coords = [P1.pos.x + 2, P1.pos.y + 6]
    def pick_up(self):
        '''
        This method is run if the player picks the item up. It is then stored in the players selected hotbar slot
        '''
        # Only attempt pickup if the item is in-world and has a mask
        if not self.visible:
            return
        #if there isnt a mask make one
        if getattr(self, "mask", None) is None:
            self.mask = pygame.mask.from_surface(self.image)
        #setting up offset to check overlap
        offset = (int(P1.pos.x - self.pos[0]), int(P1.pos.y - self.pos[1]))
        #checking overlap
        if self.mask.overlap(P1.mask, offset):
            #checking if the hotbar can take an item in the current state
            accepted = HOTBAR.pick_up_item(self)
            if accepted:
                # hide the world item and clear its mask so it no longer collides or draws
                self.visible = False
                # clear mask so overlap won't trigger again; recreate when returning to world
                self.mask.clear()
    def holding_item(self):
        '''
        This determines if the item is selected and tells the view where to put the item on the player so it looks like steve is holding it.
        '''
        if P1.image == P1.imageright:
            #setting hold coordinates if steve is facing right 
            self.hold_coords = self.hold_coords = [P1.pos.x + 2, P1.pos.y + 6]
            #setting the image to the normal image
            self.image = self.image_normal
        else:
            #setting hold coordinates if steve is facing left
            self.hold_coords = self.hold_coords = [P1.pos.x - 10, P1.pos.y + 6]
            #setting the image to the reversed image
            self.image = self.image_reversed

class interactable(pygame.sprite.Sprite):
    '''
    This class is for entities that are interactable like chests,mobs, and ore.
    '''
    def __init__(self,image,position,size, solid,reversed=False):
        '''
        Setting up an interactable sprite
        Inputs:
            image - a string representing the path to the .png file
            position - a tuple representing the x and y coordinates of the sprite in blocks (32 pixels = 1 block)
            size - size of the .png uploaded
            solid - boolean logic telling whether the player can pass through the interactable
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
        #setting position in pixels
        self.pos = [blocks_to_pixels.blocks_to_pixels(position[0]),blocks_to_pixels.blocks_to_pixels(position[1])]
    def interact(self,drop,newimage,size):
        '''
        This method takes an interactable and makes the drop item visible and turns the interactable either into the newimage or invisible
        Inputs:
            drop - the instance of the item class that is being dropped by the interactable
            newimage - a string representing the path to the png you wish to change the interatable to. Or None if you wish the iteractable to go away
            size - a tuple representing the x and y size of the newimage in blocks
        '''
        if newimage != None and self.mask.overlap(P1.mask, [int(P1.pos.x - self.pos[0]), int(P1.pos.y - self.pos[1])]):
            #loading the new image
            img = pygame.image.load(newimage).convert_alpha()
            #assigning the new image
            self.image = pygame.transform.scale(img, (blocks_to_pixels.blocks_to_pixels(size[0]),blocks_to_pixels.blocks_to_pixels(size[1])))
            if drop != None:
                #setting the item the interactable drops to visible
                drop.visible = True
            #removing the mask so you cant interact with it again
            self.mask.clear()
        elif newimage == None and self.mask.overlap(P1.mask, [int(P1.pos.x - self.pos[0]), int(P1.pos.y - self.pos[1])]):
            if drop != None:
                #setting the dropped item to visible
                drop.visible = True
            #setting the interactable to invisible
            self.visible = False
            #making it no longer solid
            self.solid = False
            #getting rid of its mask
            self.mask.clear()
    def craft(self,drop,cost):
        '''
        Determines how crafting function of crafting tables works
        Inputs:
            drop: instance of outputted item
            cost: instance of required item to get drop
        '''
        if not isinstance(cost, (list, tuple)):
            cost = [cost]
        #ensures the player is touching the crafting table
        if not self.mask.overlap(P1.mask, [self.pos[0]-P1.pos.x, self.pos[1]-P1.pos.y]):
            return
        #checking for the item needed to craft
        if all(HOTBAR.check_for_item(item) for item in cost):
            for item in cost:
                #deleting the item needed to craft
                HOTBAR.delete_item(item)
            #storing the crafted item in the hotbar
            HOTBAR.pick_up_item(drop)


def solid_mask(instance, P1):
    '''
    Turns collisions on for any entity so you cant pass through the sprite
    Inputs:
        instance: class instance of the entity
        P1: instance of the Player class in 2d_minecraft
    '''
    if P1.vel.y > 0:
        # 1. Calculate offset to check if we are touching the platform at all
        offset_x = int(instance.pos[0] - P1.pos.x)
        offset_y = int(instance.pos[1] - P1.pos.y)
                
        if P1.mask.overlap(instance.mask, (offset_x, offset_y)):
                    
            # 2. Find the EXACT pixel coordinate on the platform we hit
            instance_offset_x = int(P1.pos.x - instance.pos[0])
            instance_offset_y = int(P1.pos.y - instance.pos[1])
            instance_hit = instance.mask.overlap(P1.mask, (instance_offset_x, instance_offset_y))
                    
            if instance_hit:
                # plat_hit[1] is the local Y coordinate on the platform.
                # Add plat.pos[1] to get the absolute world Y coordinate of the floor.
                floor_y = instance.pos[1] + instance_hit[1]
                        
                # 3. Only snap if the floor is below the upper section of the player.
                # This prevents the player from instantly climbing a vertical wall
                # when walking into it, but allows them to walk on lower floors inside a large image!
                if floor_y > P1.pos.y + (P1.image.get_height() * 0.25):
                    P1.pos.y = floor_y - P1.image.get_height()
                    P1.vel.y = 0
                    P1.grounded = True
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
#creating instances of the classes for each sprite 

#Build takes 3 or 4 inputs. build("string with path to image", (location), (size), optional(reversed=True))
VILLAGEHOUSE = build("sprites\\other_sprites\\Village House.png",(10,5),(7,7))
MOUNTAIN_LEFT = build("sprites\\backgrounds\\background_cave_entrance.png", (15,0),(20,13))
MOUNTAIN_RIGHT = build("sprites\\backgrounds\\background_cave_entrance.png", (35,0), (20,13), reversed=True)
CAVE_BACKGROUND = build("sprites\\backgrounds\\cave_background.png",(27,13), (20,13))
NETHER_PORTAL = build("sprites\\other_sprites\\Netherportal_build.png",(43,13),(4,5))
FORTRESS = build("sprites\\backgrounds\\fort.png",(45,6),(WIDTH_BLOCKS,HEIGHT_BLOCKS))
STRONGHOLD = build("sprites\\backgrounds\\fort.png",(59,6),(WIDTH_BLOCKS,HEIGHT_BLOCKS))
END = build("sprites\\backgrounds\\fort.png",(73,6),(WIDTH_BLOCKS,HEIGHT_BLOCKS))

#Platform takes 3 inputs. build("string with path to image", (location), (size))
GRASS = platform("sprites\\platforms\\platform_grass.png",(0,12),(WIDTH_BLOCKS, 1))
CAVE_ENTRANCE = platform("sprites\\platforms\\platform_cave_entrance.png",(20,3),(10,13))
CAVE_CONT = platform("sprites\\platforms\\platform_cave_entrance.png",(27,6),(10,13))
CAVE_PLATFORM = platform("sprites\\platforms\\cave_platform.png",(37,18),(WIDTH_BLOCKS,1))
NETHER_PLATFORM = platform("sprites\\platforms\\netehr_platform.png",(45,18),(WIDTH_BLOCKS,1))
STRONGHOLD_PLATFORM = platform("sprites\\platforms\\netehr_platform.png",(59,18),(WIDTH_BLOCKS,1))
END_PLATFORM = platform("sprites\\platforms\\netehr_platform.png",(73,18),(WIDTH_BLOCKS,1))

#Player takes one input. Player((size)
P1 = player((1,2))

#Interactable takes 4 inputs. build("string with path to image", (location), (size), (whether or not you can pass through it))
CHEST = interactable("sprites\\other_sprites\\chest_front.png",(17,11),(1,1), False)
DIAMOND_ORE = interactable("sprites\\blocks\\diamond_ore.png", (36,17), (1,1), True) 
CRAFTING_TABLE = interactable("sprites\\blocks\\crafting_table_side.png",(40,17),(1,1), False)
BLAZE = interactable("sprites\\other_sprites\\blaze.png",(51,14),(2,4),False)
CHEST2 = interactable("sprites\\other_sprites\\chest_front.png",(54,17),(1,1),False)
CRAFTING_TABLE2 = interactable("sprites\\blocks\\crafting_table_side.png",(57,17),(1,1),False)
END_PORTAL = interactable("sprites\\other_sprites\\end_portal.png",(63,17),(5,1),True)
DRAGON = interactable("sprites\\other_sprites\\dragon.png",(77,14),(16,6),False)

#Item takes 3 inputs. build("string with path to image", (location), (size))
IRON_PICKAXE = item("sprites\\items\\iron_pickaxe.png",(18,11),(1,1))
DIAMOND = item("sprites\\items\\diamond.png",(35,17),(1,1))
DIAMOND_SWORD = item("sprites\\items\\diamond_sword.png",(41,17),(1,1))
BLAZE_ROD = item("sprites\\items\\blaze_rod.png",(51,17),(1,1))
EYE_OF_ENDER = item('sprites\\items\\ender_eye.png',(58,17),(1,1))
PEARL = item("sprites\\items\\ender_pearl.png",(55,17),(1,1))
END_CREDIT = item("sprites\\backgrounds\\end credit.png",(73,6),(640,22))

#Hotbar takes 4 inputs. build("string with path to image of whole hotbar", "string with path to image of selected hotbar slot",(location), (size))
HOTBAR = hotbar("sprites\\other_sprites\\hotbar.png", "sprites\\other_sprites\\selected_hotbar_slot.png", (WIDTH/3.3, HEIGHT-15), [135,16])
#real size 180x21

#creating sprite groups by class
builds = pygame.sprite.Group()
platforms = pygame.sprite.Group()
interactables = pygame.sprite.Group()
items = pygame.sprite.Group()

#creating a group with every sprite
all_sprites = pygame.sprite.Group()

#adding each instance of to the groups
builds.add(VILLAGEHOUSE)
builds.add(MOUNTAIN_LEFT)
builds.add(MOUNTAIN_RIGHT)
builds.add(CAVE_BACKGROUND)
builds.add(NETHER_PORTAL)
builds.add(FORTRESS)
builds.add(STRONGHOLD)
builds.add(END)
builds.add(END_CREDIT)
platforms.add(GRASS)
platforms.add(CAVE_ENTRANCE)
platforms.add(CAVE_CONT)
platforms.add(CAVE_PLATFORM)
platforms.add(NETHER_PLATFORM)
platforms.add(STRONGHOLD_PLATFORM)
platforms.add(END_PLATFORM)
interactables.add(CHEST)
interactables.add(DIAMOND_ORE)
interactables.add(CRAFTING_TABLE)
interactables.add(BLAZE)
interactables.add(CHEST2)
interactables.add(CRAFTING_TABLE2)
interactables.add(END_PORTAL)
interactables.add(DRAGON)
items.add(DIAMOND)
items.add(IRON_PICKAXE)
items.add(DIAMOND_SWORD)
items.add(BLAZE_ROD)
items.add(PEARL)
items.add(EYE_OF_ENDER)

#adding every instance to all_sprites
all_sprites.add(VILLAGEHOUSE)
all_sprites.add(MOUNTAIN_RIGHT)
all_sprites.add(FORTRESS)
all_sprites.add(CAVE_BACKGROUND)
all_sprites.add(GRASS)
all_sprites.add(MOUNTAIN_LEFT)
all_sprites.add(CHEST)
all_sprites.add(IRON_PICKAXE)
all_sprites.add(CAVE_CONT)
all_sprites.add(CAVE_ENTRANCE)
all_sprites.add(STRONGHOLD_PLATFORM)
all_sprites.add(STRONGHOLD)
all_sprites.add(BLAZE)
all_sprites.add(END)
all_sprites.add(END_PLATFORM)
all_sprites.add(CAVE_PLATFORM)
all_sprites.add(CRAFTING_TABLE)
all_sprites.add(DIAMOND)
all_sprites.add(DIAMOND_ORE)
all_sprites.add(DIAMOND_SWORD)
all_sprites.add(NETHER_PORTAL)
all_sprites.add(NETHER_PLATFORM)
all_sprites.add(CHEST2)
all_sprites.add(BLAZE_ROD)
all_sprites.add(PEARL)
all_sprites.add(DRAGON)
all_sprites.add(EYE_OF_ENDER)
all_sprites.add(CRAFTING_TABLE2)
all_sprites.add(END_PORTAL)
all_sprites.add(END_CREDIT)
all_sprites.add(P1)

while True:

    #main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
    #every tick it checks these
    P1.move()
    P1.update()
    P1.change_image()
    IRON_PICKAXE.pick_up()
    CHEST.interact(IRON_PICKAXE,"sprites\\other_sprites\\chest_front.png",(1,1))
    pygame.display.update()
    FramePerSec.tick(FPS)
    DIAMOND_ORE.interact(DIAMOND,None,(1,1))
    DIAMOND.pick_up()
    CRAFTING_TABLE.craft(DIAMOND_SWORD,[DIAMOND])
    BLAZE.interact(BLAZE_ROD,None,(2,4))
    BLAZE_ROD.pick_up()
    CHEST2.interact(PEARL,None,(1,1))
    PEARL.pick_up()
    CRAFTING_TABLE2.craft(EYE_OF_ENDER,[PEARL,BLAZE_ROD])
    EYE_OF_ENDER.pick_up()
    END_PORTAL.interact(None,"sprites\\other_sprites\\filled_end_portal.png",(5,1))
    DRAGON.interact(END_CREDIT,None,(640,22))

    #scrolling of screen
    scroll_x = int(P1.pos.x - (WIDTH / 2))
    scroll_y = 0
    if P1.pos.y > blocks_to_pixels.blocks_to_pixels(12):
        scroll_y = int(P1.pos.y - (HEIGHT/2))
    displaysurface.blit(bg_image, (0, 0)) 
    #draws all the sprites
    for entity in all_sprites:
        if entity.visible:
            draw_pos = (entity.pos[0] - scroll_x, entity.pos[1] - scroll_y)
            displaysurface.blit(entity.image, (int(draw_pos[0]), int(draw_pos[1])))
    
    #ensures hotbar stays in the same place while moving
    draw_pos = (HOTBAR.pos[0], HOTBAR.pos[1])
    displaysurface.blit(HOTBAR.image, draw_pos)
    #drawing selected hotbar slot
    displaysurface.blit(HOTBAR.s_image, HOTBAR.selected_coordinates)
    #placing items
    for i in range(9):
        slot = HOTBAR.hotbar[i]
        if slot != None:
            #slot - instance of the item in position i
            # i - slot index of instance 
            #drawing items in hotbar
            draw_pos = [HOTBAR.x_positions[i], HOTBAR.pos[1]]
            displaysurface.blit(slot.image_normal, draw_pos)
            #making steve hold the item
            if i+1 == HOTBAR.selected_slot:
                slot.holding_item()
                draw_x = slot.hold_coords[0] - scroll_x
                draw_y = slot.hold_coords[1] - scroll_y
                displaysurface.blit(slot.image, (int(draw_x), int(draw_y)))

    
    #code for displaying masks just change the sprite and it will display in red
    #display_mask(DIAMOND)

    #every tick it checks these
    """
    display_mask(P1)
    P1.move()
    P1.update()
    P1.change_image()
    IRON_PICKAXE.pick_up()
    CHEST.interact(IRON_PICKAXE,"other_sprites\\chest_front.png",(1,1))
    pygame.display.update()
    FramePerSec.tick(FPS)
    CHEST.interact(DIAMOND,None,(1,1))
    """