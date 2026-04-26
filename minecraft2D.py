import pygame
import sys
import random
import blocks_to_pixels
from pygame.locals import *
import hotbar
import player
import item
import platform_func
import interactable
import build
import collisions
import build
import mob

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
        
#creating instances of the classes for each sprite 

#Build takes 3 or 4 inputs. build("string with path to image", (location), (size), optional(reversed=True))
VILLAGE_HOUSE = build.Build("sprites\\other_sprites\\Village House.png",(10,5),(7,7))
END_BACKGROUND = build.Build("sprites\\backgrounds\\background_end.png", (68,6),(20,30))
MOUNTAIN_LEFT = build.Build("sprites\\backgrounds\\background_cave_entrance.png", (15,0),(20,13))
MOUNTAIN_RIGHT = build.Build("sprites\\backgrounds\\background_cave_entrance.png", (35,0), (20,13), reversed=True)
CAVE_BACKGROUND = build.Build("sprites\\backgrounds\\cave_background.png",(27,13), (20,13))
NETHER_PORTAL = build.Build("sprites\\other_sprites\\Netherportal_build.png",(43,13),(4,5))
FORTRESS = build.Build("sprites\\backgrounds\\fort.png",(45,6),(WIDTH_BLOCKS,HEIGHT_BLOCKS))
STRONGHOLD = build.Build("sprites\\backgrounds\\fort.png",(59,6),(WIDTH_BLOCKS,HEIGHT_BLOCKS))
END = build.Build("sprites\\backgrounds\\fort.png",(73,6),(WIDTH_BLOCKS,HEIGHT_BLOCKS))
UNDERGROUND_BACKGROUND = build.Build("sprites\\backgrounds\\underground_background.png",(17,13),(WIDTH_BLOCKS,HEIGHT_BLOCKS))
UNDERGROUND_BACKGROUND2 = build.Build("sprites\\backgrounds\\underground_background.png",(25,18),(WIDTH_BLOCKS,HEIGHT_BLOCKS))
UNDERGROUND_NETHER_BACKGROUND = build.Build("sprites\\backgrounds\\underground_nether_background.png",(45,19),(WIDTH_BLOCKS,HEIGHT_BLOCKS))
UNDERGROUND_NETHER_BACKGROUND2 = build.Build("sprites\\backgrounds\\underground_nether_background.png",(48,18),(WIDTH_BLOCKS,HEIGHT_BLOCKS))

#Platform takes 3 inputs. build("string with path to image", (location), (size))
GRASS = platform_func.Platform("sprites\\platforms\\platform_grass.png",(0,12),(WIDTH_BLOCKS, 1))
CAVE_ENTRANCE = platform_func.Platform("sprites\\platforms\\platform_cave_entrance.png",(20,3),(10,13))
CAVE_CONT = platform_func.Platform("sprites\\platforms\\platform_cave_entrance.png",(27,6),(10,13))
CAVE_PLATFORM = platform_func.Platform("sprites\\platforms\\cave_platform.png",(37,18),(WIDTH_BLOCKS,1))
NETHER_PLATFORM = platform_func.Platform("sprites\\platforms\\netehr_platform.png",(45,18),(WIDTH_BLOCKS,1))
STRONGHOLD_PLATFORM = platform_func.Platform("sprites\\platforms\\netehr_platform.png",(59,18),(WIDTH_BLOCKS,1))
END_PLATFORM = platform_func.Platform("sprites\\platforms\\end_platform.png",(68,7),(WIDTH_BLOCKS,HEIGHT_BLOCKS))
LOWER_END_PLATFORM = platform_func.Platform("sprites\\platforms\\lower_end_platform.png",(68,12),(WIDTH_BLOCKS,HEIGHT_BLOCKS))

#Player takes one input. Player((size)
P1 = player.Player((1,2))

#Item takes 3 inputs. build("string with path to image", (location), (size))
IRON_PICKAXE = item.Item("sprites\\items\\iron_pickaxe.png",(18,11),(1,1))
DIAMOND = item.Item("sprites\\items\\diamond.png",(35,17),(1,1))
DIAMOND_SWORD = item.Item("sprites\\items\\diamond_sword.png",(41,17),(1,1))
BLAZE_ROD = item.Item("sprites\\items\\blaze_rod.png",(51,17),(1,1))
EYE_OF_ENDER = item.Item('sprites\\items\\ender_eye.png',(58,17),(1,1))
PEARL = item.Item("sprites\\items\\ender_pearl.png",(55,17),(1,1))
END_CREDIT = item.Item("sprites\\backgrounds\\end credit.png",(73,6),(40/1.6,22/1.6))

#Interactable takes 4 inputs. build("string with path to image", (location), (size), (required item), (whether or not you can pass through it))
#image,position,size, solid,requirement, reversed=False
CHEST = interactable.Interactable("sprites\\other_sprites\\chest_front.png",(17,11),(1,1), False, None)
DIAMOND_ORE = interactable.Interactable("sprites\\blocks\\diamond_ore.png", (36,17), (1,1), True, IRON_PICKAXE) 
CRAFTING_TABLE = interactable.Interactable("sprites\\blocks\\crafting_table_side.png",(40,17),(1,1), False,None)
CHEST2 = interactable.Interactable("sprites\\other_sprites\\chest_front.png",(54,17),(1,1),False,None)
CRAFTING_TABLE2 = interactable.Interactable("sprites\\blocks\\crafting_table_side.png",(57,17),(1,1),False,None)
END_PORTAL = interactable.Interactable("sprites\\other_sprites\\end_portal.png",(63,17),(5,1),True,EYE_OF_ENDER)

#Mobs image,position,size,requirement,health,health_size
DRAGON = mob.Mob("sprites\\other_sprites\\dragon.png",(77,11),(16,6),DIAMOND_SWORD, 8,(10,10))
BLAZE = mob.Mob("sprites\\other_sprites\\blaze.png",(51,14),(2,4), DIAMOND_SWORD, 20,(10,10))

#Hotbar takes 4 inputs. build("string with path to image of whole hotbar", "string with path to image of selected hotbar slot",(location), (size))
HOTBAR = hotbar.Hotbar("sprites\\other_sprites\\hotbar.png", "sprites\\other_sprites\\selected_hotbar_slot.png", (WIDTH/3.3, HEIGHT-15), [135,16], WIDTH)
#real size 180x21
#creating sprite groups by class
builds = pygame.sprite.Group()
platforms = pygame.sprite.Group()
interactables = pygame.sprite.Group()
items = pygame.sprite.Group()
mobs = pygame.sprite.Group()

#creating a group with every sprite
all_sprites = pygame.sprite.Group()

#adding each instance of to the groups
builds.add(VILLAGE_HOUSE)
builds.add(MOUNTAIN_LEFT)
builds.add(MOUNTAIN_RIGHT)
builds.add(CAVE_BACKGROUND)
builds.add(END_BACKGROUND)
builds.add(NETHER_PORTAL)
builds.add(FORTRESS)
builds.add(STRONGHOLD)
builds.add(END)
builds.add(END_CREDIT)
builds.add(UNDERGROUND_BACKGROUND)
builds.add(UNDERGROUND_BACKGROUND2)
builds.add(UNDERGROUND_NETHER_BACKGROUND)
builds.add(UNDERGROUND_NETHER_BACKGROUND2)
platforms.add(GRASS)
platforms.add(CAVE_ENTRANCE)
platforms.add(CAVE_CONT)
platforms.add(CAVE_PLATFORM)
platforms.add(NETHER_PLATFORM)
platforms.add(STRONGHOLD_PLATFORM)
platforms.add(END_PLATFORM)
platforms.add(LOWER_END_PLATFORM)
interactables.add(CHEST)
interactables.add(DIAMOND_ORE)
interactables.add(CRAFTING_TABLE)
interactables.add(CHEST2)
interactables.add(CRAFTING_TABLE2)
interactables.add(END_PORTAL)
mobs.add(DRAGON)
mobs.add(BLAZE)
items.add(DIAMOND)
items.add(IRON_PICKAXE)
items.add(DIAMOND_SWORD)
items.add(BLAZE_ROD)
items.add(PEARL)
items.add(EYE_OF_ENDER)

#adding every instance to all_sprites
all_sprites.add(VILLAGE_HOUSE)
all_sprites.add(MOUNTAIN_RIGHT)
all_sprites.add(FORTRESS)
all_sprites.add(UNDERGROUND_BACKGROUND)
all_sprites.add(CAVE_BACKGROUND)
all_sprites.add(GRASS)
all_sprites.add(MOUNTAIN_LEFT)
all_sprites.add(CHEST)
all_sprites.add(IRON_PICKAXE)
all_sprites.add(CAVE_CONT)
all_sprites.add(CAVE_ENTRANCE)
all_sprites.add(UNDERGROUND_BACKGROUND2)
all_sprites.add(STRONGHOLD_PLATFORM)
all_sprites.add(STRONGHOLD)
all_sprites.add(BLAZE)
all_sprites.add(END)
all_sprites.add(CAVE_PLATFORM)
all_sprites.add(CRAFTING_TABLE)
all_sprites.add(DIAMOND)
all_sprites.add(DIAMOND_ORE)
all_sprites.add(DIAMOND_SWORD)
all_sprites.add(NETHER_PORTAL)
all_sprites.add(UNDERGROUND_NETHER_BACKGROUND)
all_sprites.add(NETHER_PLATFORM)
all_sprites.add(UNDERGROUND_NETHER_BACKGROUND2)
all_sprites.add(CHEST2)
all_sprites.add(BLAZE_ROD)
all_sprites.add(END_BACKGROUND)
all_sprites.add(END_PLATFORM)
all_sprites.add(LOWER_END_PLATFORM)
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
                P1.jump(platforms)
    #every tick it checks these
    P1.move(HOTBAR)
    P1.update(platforms, interactables, collisions.solid_mask)
    P1.change_image()
    IRON_PICKAXE.pick_up(HOTBAR,P1)
    CHEST.interact(P1, IRON_PICKAXE,"sprites\\other_sprites\\chest_front.png",(1,1), HOTBAR)
    pygame.display.update()
    FramePerSec.tick(FPS)
    DIAMOND_ORE.interact(P1,DIAMOND,None,(1,1), HOTBAR)
    DIAMOND.pick_up(HOTBAR,P1)
    CRAFTING_TABLE.craft(DIAMOND_SWORD,[DIAMOND],HOTBAR,P1)
    BLAZE.damage(P1, HOTBAR, BLAZE_ROD)
    BLAZE_ROD.pick_up(HOTBAR,P1)
    CHEST2.interact(P1,PEARL,None,(1,1), HOTBAR)
    PEARL.pick_up(HOTBAR,P1)
    CRAFTING_TABLE2.craft(EYE_OF_ENDER, [PEARL,BLAZE_ROD], HOTBAR, P1)
    EYE_OF_ENDER.pick_up(HOTBAR,P1)
    END_PORTAL.interact(P1,None,"sprites\\other_sprites\\filled_end_portal.png",(5,1), HOTBAR)
    DRAGON.damage(P1, HOTBAR, BLAZE_ROD, True)

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
                slot.holding_item(P1)
                draw_x = slot.hold_coords[0] - scroll_x
                draw_y = slot.hold_coords[1] - scroll_y
                displaysurface.blit(slot.image, (int(draw_x), int(draw_y)))
    #checking for end
    if DRAGON.end == True:
        #removing all sprites so next draw contains nothing
        all_sprites.empty()
        #drawing the credits
        displaysurface.blit(END_CREDIT.image_normal, (blocks_to_pixels.blocks_to_pixels(-2),0))