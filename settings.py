import pygame

from utilities import *
from game import *



# Window settings
GRID_SIZE = 64
WIDTH = 26 * GRID_SIZE
HEIGHT = 12 * GRID_SIZE
TITLE = "My Awesome Game"
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
SKY_BLUE = (135, 200, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40,40,40)
RED = (125,0,0)

FONT_SM = pygame.font.Font(None, 20)

# Images
''' hero '''
HERO_IDLE_R = [load_image('assets/images/characters/B_Idle1.png'),
load_image('assets/images/characters/B_Idle2.png'),
load_image('assets/images/characters/B_Idle3.png')]
HERO_IDLE_L = [flip_x(img)for img in HERO_IDLE_R]

HERO_WALK_R = [load_image('assets/images/characters/B_Walk1.png'),
load_image('assets/images/characters/B_Walk2.png'),
load_image('assets/images/characters/B_Walk3.png'),
load_image('assets/images/characters/B_Walk4.png')]
HERO_WALK_L = [flip_x(img)for img in HERO_WALK_R]

HERO_JUMP_R = [load_image('assets/images/characters/B_Jump1.png'),
load_image('assets/images/characters/B_Jump2.png'),
load_image('assets/images/characters/B_Jump3.png')]
HERO_JUMP_L = [flip_x(img)for img in HERO_JUMP_R]

HERO_FALL_R = [load_image('assets/images/characters/B_Fall1.png'),
load_image('assets/images/characters/B_Fall2.png'),
load_image('assets/images/characters/B_Fall3.png')]
HERO_FALL_L = [flip_x(img)for img in HERO_FALL_R]

HERO_DASH_R = [load_image('assets/images/characters/B_Dash1.png'),
load_image('assets/images/characters/B_Dash2.png'),
load_image('assets/images/characters/B_Dash3.png'),
load_image('assets/images/characters/B_Dash4.png')]
HERO_DASH_L = [flip_x(img)for img in HERO_DASH_R]

HERO_STRIKE_R = [load_image('assets/images/characters/B_Strike1.png'),
load_image('assets/images/characters/B_Strike2.png'),
load_image('assets/images/characters/B_Strike3.png'),
load_image('assets/images/characters/B_Strike4.png')]
HERO_STRIKE_L = [flip_x(img)for img in HERO_STRIKE_R]

HERO_DEATH = [load_image('assets/images/characters/B_Death.png')]

slash1 = 'assets/images/characters/slash1.png'
slash2 = 'assets/images/characters/slash2.png'
slash3 = 'assets/images/characters/slash3.png'
slash4 = 'assets/images/characters/slash4.png'

SLASH = [slash1,slash2,slash3,slash4]


'''Boss'''
BOSS_STATUE = [load_image('assets/images/characters/E_Statue.png')]

BOSS_START = [load_image('assets/images/characters/E_Wait.png'),
              load_image('assets/images/characters/E_Wait2.png'),
              load_image('assets/images/characters/E_Wait3.png'),
              load_image('assets/images/characters/E_Wait4.png'),]

BOSS_IDLE_R = [load_image('assets/images/characters/E_Idle.png')]
BOSS_IDLE_L = [flip_x(img)for img in BOSS_IDLE_R]

BOSS_WALK_R = [load_image('assets/images/characters/E_Idle.png'),
               load_image('assets/images/characters/E_Ready1.png'),
               load_image('assets/images/characters/E_Ready2.png'),
               load_image('assets/images/characters/E_Ready3.png'),
               load_image('assets/images/characters/E_Ready4.png'),
               load_image('assets/images/characters/E_Ready5.png'),
               load_image('assets/images/characters/E_Ready6.png'),
               load_image('assets/images/characters/E_Ready7.png'),
               load_image('assets/images/characters/E_Ready8.png'),
               load_image('assets/images/characters/E_Ready9.png'),
               load_image('assets/images/characters/E_Ready10.png'),
               load_image('assets/images/characters/E_Lunge1.png'),
               load_image('assets/images/characters/E_Lunge2.png'),
               load_image('assets/images/characters/E_Lunge3.png'),
               load_image('assets/images/characters/E_Lunge4.png'),
               load_image('assets/images/characters/E_Lunge5.png'),
               load_image('assets/images/characters/E_Lunge6.png'),
               load_image('assets/images/characters/E_Lunge7.png'),
               load_image('assets/images/characters/E_Stop1.png'),
               load_image('assets/images/characters/E_Stop2.png'),
               load_image('assets/images/characters/E_Stop3.png'),
               load_image('assets/images/characters/E_Stop4.png'),
               load_image('assets/images/characters/E_Stop5.png'),
               load_image('assets/images/characters/E_Stop6.png'),
               load_image('assets/images/characters/E_Stop7.png'),]
BOSS_WALK_L = [flip_x(img)for img in BOSS_WALK_R]

BOSS_DEATH = [load_image('assets/images/characters/E_Death1.png'),
               load_image('assets/images/characters/E_Death2.png'),
               load_image('assets/images/characters/E_Death3.png'),
               load_image('assets/images/characters/E_Death4.png'),
               load_image('assets/images/characters/E_Death5.png'),
               load_image('assets/images/characters/E_Death6.png'),
              load_image('assets/images/characters/E_Death6.png')]

BOSS_PUNCH_R = [load_image('assets/images/characters/E_Punch1.png'),
               load_image('assets/images/characters/E_Punch2.png'),
               load_image('assets/images/characters/E_Punch3.png'),
               load_image('assets/images/characters/E_Punch4.png'),
               load_image('assets/images/characters/E_Punch5.png'),
               load_image('assets/images/characters/E_Punch6.png'),
              load_image('assets/images/characters/E_Punch7.png'),
              load_image('assets/images/characters/E_Punch8.png'),
              load_image('assets/images/characters/E_Punch9.png'),
              load_image('assets/images/characters/E_Punch10.png'),
              load_image('assets/images/characters/E_Punch11.png'),
              load_image('assets/images/characters/E_Punch12.png'),
              load_image('assets/images/characters/E_Punch13.png'),
              load_image('assets/images/characters/E_Punch14.png'),
              load_image('assets/images/characters/E_Punch15.png')]
BOSS_PUNCH_L = [flip_x(img)for img in BOSS_PUNCH_R]

BOSS_AIR_R = [load_image('assets/images/characters/E_Air1.png'),
              load_image('assets/images/characters/E_Air2.png'),
              load_image('assets/images/characters/E_Air3.png'),
              load_image('assets/images/characters/E_Air4.png'),
              load_image('assets/images/characters/E_Air5.png'),
              load_image('assets/images/characters/E_Air6.png'),
              load_image('assets/images/characters/E_Air7.png'),
              load_image('assets/images/characters/E_Air8.png'),
              load_image('assets/images/characters/E_Air9.png'),
              load_image('assets/images/characters/E_Air10.png'),
              load_image('assets/images/characters/E_Air11.png'),
              load_image('assets/images/characters/E_Air12.png'),
              load_image('assets/images/characters/E_Air13.png'),
              load_image('assets/images/characters/E_Air14.png'),
              load_image('assets/images/characters/E_Air15.png'),
              load_image('assets/images/characters/E_Air16.png'),
              load_image('assets/images/characters/E_Air17.png'),
              load_image('assets/images/characters/E_Air18.png'),
              load_image('assets/images/characters/E_Air19.png'),
              load_image('assets/images/characters/E_Air19.png'),
              load_image('assets/images/characters/E_Air20.png')]
BOSS_AIR_L = [flip_x(img)for img in BOSS_AIR_R]

BOSS_SCREECH = [load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png'),
                load_image('assets/images/characters/E_Screech.png')]

'''dummy'''
DUMMY = [load_image('assets/images/characters/Dummy1.png'),
              load_image('assets/images/characters/Dummy2.png')]

''' tiles '''
GRASS_IMG = load_image('assets/images/tiles/block.png')
BLOCK_IMG = load_image('assets/images/tiles/block.png')
grass_img = load_image('assets/images/tiles/grass_dirt.png')
stone_img = load_image('assets/images/tiles/stone.png')

''' items '''
GEM_IMG = load_image('assets/images/items/diamond.png')

HEART_IMG = load_image('assets/images/items/health.png')

'''bg'''
BG = load_image('assets/images/backgrounds/bg.png')
LOWBG = load_image('assets/images/backgrounds/Lowbg.png')
TITLE_IMG = load_image('assets/images/backgrounds/Title.png')
SPACE_IMG = load_image('assets/images/backgrounds/Space.png')
VIGNETTE = load_image('assets/images/backgrounds/vignette.png')
VIGNETTE2 = load_image('assets/images/backgrounds/vignette2.png')
TRANSITION = load_image('assets/images/backgrounds/transition.png')
WHITE_IMG = load_image('assets/images/backgrounds/WHITE.png')
PAUSE_IMG = load_image('assets/images/backgrounds/Pause.png')

# Sounds
JUMP_SND = 'assets/sounds/jump.wav'
GEM_SND = 'assets/sounds/collect_point.wav'

# Music
TITLE_MUSIC = 'assets/music/calm_happy.ogg'
MAIN_THEME = 'assets/music/cooking_mania.wav'


# Levels
STARTING_LEVEL = 1

LEVELS = ['assets/levels/world-1.json',
          'assets/levels/world-2.json',
          'assets/levels/world-3.json']


# Stages
START = 0
PLAYING = 1
PAUSE = 2
LEVEL_COMPLETE = 3
WIN = 4
LOSE = 5





# Gameplay settings
HERO_HEARTS = 10
HERO_STRIKE_SPEED = 1
HERO_SPEED = 15
HERO_JUMP_POWER = 21
HERO_HASTE = 8
TERMINAL_VEL = 25
GRAVITY = .5

BOSS_HEARTS = 300
