# Imports
import json
import pygame
import random

from entities import *
from overlays import *
from settings import *
from utilities import *


# Main game class 
class Game:

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()

        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.display = pygame.Surface((200,300))

        self.load_assets()
        self.make_overlays()
        self.new_game()

        self.debug = False
        self.screen_shake = 0
        self.render_offset = [0,0]
        
        self.hero.strike_cooldown = 0

        self.health_x = 0
        self.health_y = 0

        self.health_x2 = 0
        self.health_y2 = 0
    
        
        self.particles = []
        self.dash_particles = []
        self.mouse_particles = []
        self.health_particles2 = []
        self.health_particles = []
        self.white_dust = []
        self.black_dust = []
        self.spark_particles = []
        self.red_spark_particles = []
        self.enemy_particles = []
        self.ticks = 0
        self.lose_ticks = 0
        self.win_ticks = 0
        self.start_screen_ticks = 1
        self.destruct = 0

        self.points = 0

        self.COLOR = [150,0,0]

        self.fighting = False
        self.transition_x = -3000
        self.transition = False

        self.death_count = 0

        self.jump_boost = 0


    def load_assets(self):
        self.hero_img = HERO_IDLE_R
        self.grass_dirt_img = GRASS_IMG
        self.block_img = BLOCK_IMG
        self.gem_img = GEM_IMG
        self.grass = grass_img
        self.stone = stone_img

        self.boss_img = BOSS_START
        self.dummy_img = DUMMY
        self.statue_img = BOSS_STATUE

        self.slash1 = Image(SLASH[0])

        self.swing_sfx = Sound('assets/sounds/swing.ogg')
        self.dash_sfx = Sound('assets/sounds/dash.ogg')
        self.death1_sfx = Sound('assets/sounds/death1.ogg',.2)
        self.death2_sfx = Sound('assets/sounds/death2.ogg')
        self.screech_sfx = Sound('assets/sounds/screech.ogg',.2)
        self.hit_sfx = Sound('assets/sounds/hit.ogg')
        self.airboom_sfx = Sound('assets/sounds/airboom.ogg',.2)


    def make_overlays(self):
        self.title_screen = TitleScreen(self)
        self.win_screen = WinScreen(self)
        self.lose_screen = LoseScreen(self)
        self.level_complete_screen = LevelCompleteScreen(self)
        self.pause_screen = PauseScreen(self)
        self.hud = HUD(self)
        self.grid = Grid(self)

        
        
    def new_game(self):
        # Make the hero here so it persists across levels
        self.player = pygame.sprite.Group()
        self.hero = Hero(self, self.hero_img)
        self.player.add(self.hero)

        # Go to first level

        self.hero.dash_cooldown = 4
        self.lose_ticks = 0
        self.win_ticks = 0
        self.fighting = False
        self.transition_x = -3000
        self.transition = False
        self.debug = False

        
        self.stage = START
        self.level = STARTING_LEVEL
        self.load_level()

    def load_level(self):
        # Make sprite groups
        self.attack = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.ground = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dummy = pygame.sprite.Group()
        self.statue = pygame.sprite.Group()

        if self.level == 1:
            self.music = Music("assets/music/training.ogg",.05)
            self.music.play()
        else:
            self.music = Music("assets/music/battle.ogg",.05)
            self.music.play()

        # Load the level data
        with open(LEVELS[self.level - 1]) as f:
            self.data = json.load(f)

        # World settings
        self.world_width = self.data['width'] * GRID_SIZE
        self.world_height = self.data['height'] * GRID_SIZE

        # Position the hero
        loc = self.data['start']
        self.hero.move_to(loc)

        # Add the platforms
        if 'ground' in self.data:   
            for loc in self.data['ground']:
                self.ground.add( Platform(self, self.block_img, loc) )

        if 'blocks' in self.data:    
            for loc in self.data['blocks']:
                self.platforms.add( Platform(self, self.block_img, loc) )

        if 'stone' in self.data:    
            for loc in self.data['stone']:
                self.platforms.add( Platform(self, self.stone, loc) )

        if 'dirt' in self.data:    
            for loc in self.data['dirt']:
                self.platforms.add( Platform(self, self.grass, loc) )


        # Add enemies
        r = random.randrange(1,69)
        if 'boss' in self.data:
            for loc in self.data['boss']:
                self.enemies.add( Boss(self, self.boss_img, loc) )
                # The 1-69 Event
                if r == 1:
                    self.enemies.add( Boss(self, self.boss_img, loc) )
                    self.enemies.add( Boss(self, self.boss_img, loc) )
                    self.enemies.add( Boss(self, self.boss_img, loc) )
                    self.enemies.add( Boss(self, self.boss_img, loc) )
                    self.hero.hearts = 690
                    self.hero.speed = 420/12
                    self.jump_boost= 69

        if 'dummy' in self.data:
            for loc in self.data['dummy']:
                self.dummy.add( Dummy(self, self.dummy_img, loc) )

        # Misc
        if 'statue' in self.data:
            for loc in self.data['statue']:
                self.statue.add( Statue(self, self.statue_img, loc) )  
    
        # Make one big sprite group for easy updating and drawing
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.platforms, self.ground,self.attack, self.enemies, self.player,self.dummy,self.statue)
        

    def start_level(self):
        self.stage = PLAYING

    def toggle_pause(self):
        if self.stage == PLAYING:
            self.stage = PAUSE
        elif self.stage == PAUSE:
            self.stage = PLAYING

    def complete_level(self):
        self.stage = LEVEL_COMPLETE

    def advance(self):
        self.level += 1
        self.load_level()
        self.start_level()

    def win(self):
        self.stage = WIN

    def lose(self):
        self.stage = LOSE

    def process_input(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                # start/restart
                if self.stage == START and self.start_screen_ticks > 100:
                    if event.key == pygame.K_SPACE:
                        self.start_level()
                elif self.stage in [WIN, LOSE]:
                    if event.key == pygame.K_r:
                        self.new_game()

                # pause/unpause
                elif event.key == pygame.K_p:
                    self.toggle_pause()

                elif event.key == pygame.K_o:
                    if self.debug == False:
                        self.debug = True
                    else:
                        self.debug = False

                elif event.key == pygame.K_SPACE:
                    self.hero.dash_cooldown = 0
                    self.hero.jump()
                                    
                    
                # actual gameplay
                
                elif self.stage == PLAYING:
                    if event.key == pygame.K_LSHIFT:
                        if self.hero.dash_cooldown == 0 and self.hero.can_dash == True and pressed[pygame.K_a] and pressed[pygame.K_d]:
                            pass
                        elif self.hero.dash_cooldown == 0 and self.hero.can_dash == True and pressed[pygame.K_a]:
                            self.hero.anim_index = -1
                            self.hero.dash_left()
                            self.hero.can_dash = False
                            self.hero.dash_cooldown = 15
                        elif self.hero.dash_cooldown == 0 and self.hero.can_dash == True and pressed[pygame.K_d]:
                            self.hero.anim_index = -1
                            self.hero.dash_right()
                            self.hero.can_dash = False
                            self.hero.dash_cooldown = 15
                        elif len(self.attack) == 0 and self.hero.strike_cooldown <= 0 and pressed[pygame.K_k]:
                            self.hero.attack()

            b1,b2,b3 = pygame.mouse.get_pressed(3)
            if self.stage == PLAYING:
                if b1 == True and len(self.attack) == 0 and self.hero.strike_cooldown <= 0:
                    self.hero.attack()
                

        # player movement
        if self.stage == PLAYING:
                
            pressed = pygame.key.get_pressed()
            if self.hero.dash_cooldown == 0:
                if pressed[pygame.K_a] and pressed[pygame.K_d]:
                    self.hero.stop()
                elif pressed[pygame.K_a]:
                    self.hero.go_left()
                elif pressed[pygame.K_d]:
                    self.hero.go_right()
                else:
                    self.hero.stop()

            if pressed[pygame.K_k] == True and len(self.attack) == 0 and self.hero.strike_cooldown <= 0:
                    self.hero.strike_cooldown = HERO_HASTE
                    self.hero.attack()
                    
                
            if not pressed[pygame.K_SPACE]:
                self.hero.vy += 3

    def run_screen_shake(self):
        if self.screen_shake > 0:
            self.screen_shake -= 1

        self.render_offset = [0,0]
        if self.screen_shake:
            self.render_offset[0] = random.randint(-5,5)
            self.render_offset[1] = random.randint(-5,5)


    def run_cooldowns(self):
        self.hero.dash_cooldown -= 1
        if self.hero.dash_cooldown < 0:
            self.hero.dash_cooldown = 0

        self.hero.strike_cooldown -= 1
        if self.hero.strike_cooldown < 0:
            self.hero.strike_cooldown = 0

    def draw_particles(self):
        offset_x,offset_y = self.get_offsets()
        for particle in self.particles:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= self.destruct
            pygame.draw.circle(self.screen, BLACK, [(int(particle[0][0])),int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)
        if self.stage == LOSE:
            self.particles.append([[self.hero.rect.centerx - offset_x,self.hero.rect.centery - offset_y+8],[random.randint(0,300)/10 -15, random.randint(0,50)/10-2.5 ], self.hero.dash_cooldown/2])
            for particle in self.particles:
                particle[0][0] += particle [1][0]
                particle[0][1] += particle [1][1]
                particle[2] -= self.destruct
                pygame.draw.circle(self.screen, WHITE, [int(particle[0][0]),int(particle[0][1])], int(particle[2]))
                if particle[2] <= 0:
                    self.particles.remove(particle)
        '''
        for slash in self.attack:
            self.dash_particles.append([[slash.rect.centerx- offset_x,slash.rect.centery- offset_y],[10, random.randint(0,50)/10 -2.5], random.randint(2,4)])
            for particle in self.dash_particles:
                particle[0][0] += particle [1][0]
                particle[0][1] += particle [1][1]
                particle[2] -= .05
                particle[1][1] += 1
                pygame.draw.circle(self.screen, BLACK, [int(particle[0][0]),int(particle[0][1])], int(particle[2]))
                if particle[2] <= 0:
                    self.dash_particles.remove(particle)
        
        self.rain_particles.append([[650,150],[0, 10], random.randint(4,15)])
        for particle in self.rain_particles:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .5
            pygame.draw.circle(self.screen, BLACK, [int(particle[0][0]),int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.rain_particles.remove(particle)

        self.fountain_particles.append([[850,250],[random.randrange(-5,5)/10, (random.randrange(-5,5)/10) - 5], random.randint(4,6)])
        for particle in self.fountain_particles:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .035
            particle[1][1] += .1
            pygame.draw.circle(self.screen, BLACK, [int(particle[0][0]),int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.fountain_particles.remove(particle)'''
        pygame.mouse.set_visible(False)
        mx,my = pygame.mouse.get_pos()
        self.mouse_particles.append([[mx,my],[random.randint(-5,5), random.randint(-5,5)], random.randint(6,8)])
        for particle in self.mouse_particles:
            particle[2] -= 1
            pygame.draw.circle(self.screen, BLACK, [int(particle[0][0]),int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.mouse_particles.remove(particle)

    def dust_overlay(self):
        offset_x,offset_y = self.get_offsets()
        self.black_dust.append([[random.randint(-WIDTH,WIDTH+500),random.randint(HEIGHT,HEIGHT*2)],[random.randint(2,5)+random.randint(0,10)/10,-5], random.randint(2,5)])
        for particle in self.black_dust:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .01
            pygame.draw.circle(self.screen, BLACK, [int(particle[0][0])- offset_x,int(particle[0][1])- offset_y], int(particle[2]))
            if len(self.black_dust)>1:
                if particle[0][0] > WIDTH+500 or particle[2] <= 0:
                    self.black_dust.remove(particle)

        if len(self.white_dust) < 65:
            self.white_dust.append([[random.randint(-WIDTH,WIDTH+500),random.randint(HEIGHT,HEIGHT*2)],[random.randint(2,5)+random.randint(0,10)/10,-5], random.randint(2,5)])
        for particle in self.white_dust:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .01
            pygame.draw.circle(self.screen, WHITE, [int(particle[0][0])- offset_x,int(particle[0][1])- offset_y], int(particle[2]))
            if len(self.white_dust)>1:
                if particle[0][0] > WIDTH+500 or particle[2] <= 0:
                    self.white_dust.remove(particle)

    def draw_spark_particles(self):
        offset_x,offset_y = self.get_offsets()
        for particle in self.spark_particles:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .05
            particle[1][1] += .2
            pygame.draw.circle(self.screen, WHITE, [int(particle[0][0])- offset_x,int(particle[0][1])- offset_y], int(particle[2]))
            if len(self.spark_particles)>1:
                if particle[0][0] > WIDTH+500 or particle[2] <= 0:
                    self.spark_particles.remove(particle)

    def draw_red_spark_particles(self):
        offset_x,offset_y = self.get_offsets()
        for particle in self.red_spark_particles:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .05
            particle[1][1] += .2
            pygame.draw.circle(self.screen, RED, [int(particle[0][0])- offset_x,int(particle[0][1])- offset_y], int(particle[2]))
            if len(self.red_spark_particles)>1:
                if particle[0][0] > WIDTH+500 or particle[2] <= 0:
                    self.red_spark_particles.remove(particle)

    def draw_enemy_particles(self):
        offset_x,offset_y = self.get_offsets()
        for particle in self.enemy_particles:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .01
            pygame.draw.circle(self.screen, BLACK, [int(particle[0][0])- offset_x,int(particle[0][1])- offset_y], int(particle[2]))
            if len(self.enemy_particles)>1:
                if particle[2] <= 0:
                    self.enemy_particles.remove(particle)

        for particle in self.enemy_particles:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .05
            pygame.draw.circle(self.screen, WHITE, [int(particle[0][0])- offset_x,int(particle[0][1])- offset_y], int(particle[2]))
            if len(self.enemy_particles)>1:
                if particle[2] <= 0:
                    self.enemy_particles.remove(particle)

    
    def draw_health_particles(self):        
        offset_x,offset_y = self.get_offsets()
        if len(self.health_particles2)<20:
            self.health_particles2.append([[-75,random.randint(40,85)],[random.randint(5,45)/10,0], random.randint(2,5)])
        for particle in self.health_particles2:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .02
            pygame.draw.circle(self.screen, WHITE, [int(particle[0][0]),int(particle[0][1])], int(particle[2]))
            if len(self.health_particles2)>1:
                if particle[2] <= 0:
                    self.health_particles2.remove(particle)

        if len(self.health_particles)<20:
            self.health_particles.append([[-10,random.randint(35,90)],[random.randint(2,10)+random.randint(0,10)/10,0], random.randint(4,7)])
        for particle in self.health_particles:
            particle[0][0] += particle [1][0]
            particle[0][1] += particle [1][1]
            particle[2] -= .08
            pygame.draw.circle(self.screen, BLACK, [int(particle[0][0]),int(particle[0][1])], int(particle[2]))
            if len(self.health_particles)>1:
                if particle[0][0] > WIDTH+500 or particle[2] <= 0:
                    self.health_particles.remove(particle)


    def count_ticks(self):
        self.ticks += 1
        if self.ticks > 100:
            self.ticks = 0
        if self.stage == START:
            self.start_screen_ticks += 6
        else:
            self.start_screen_ticks -= 3
        if self.start_screen_ticks >= 255:
            self.start_screen_ticks = 255
        if self.start_screen_ticks <= 0:
            self.start_screen_ticks = 0

        if self.transition == True:
            self.transition_x += 200
        
        if self.transition_x > WIDTH:
            self.transition_x = WIDTH
        
            
     
    def update(self):
        if self.stage == PLAYING:
            self.run_cooldowns()
            self.all_sprites.update()
        self.run_screen_shake()

    def get_offsets(self):
        offset_threshold = 2.44
        half_threshold = offset_threshold/2
        y_thres = 1.65
        if self.hero.rect.centerx < WIDTH/offset_threshold:
            offset_x = 0
        elif self.hero.rect.centerx > self.world_width - WIDTH/offset_threshold:
            offset_x = self.world_width - WIDTH/half_threshold
        else:
            offset_x = self.hero.rect.centerx - WIDTH/offset_threshold
            

        if self.hero.rect.centery > HEIGHT/y_thres:
            offset_y = 0
        elif self.hero.rect.centery > self.world_height - HEIGHT/y_thres:
            offset_y = self.world_height - HEIGHT/(y_thres/2)
        else:
            offset_y = self.hero.rect.centery - HEIGHT/y_thres

        return offset_x/2, offset_y/2

    def render(self):
        offset_x,offset_y = self.get_offsets()
        if self.debug == False:
            self.screen.fill(WHITE)
            self.screen.blit(BG,[0,0])
            '''if self.hero.hearts == 1:
               self.screen.blit(LOWBG,[0,0])''' 
        if self.level != 3:
            TITLE_IMG.set_alpha(self.start_screen_ticks)
            self.screen.blit(TITLE_IMG,[0,0])
            SPACE_IMG.set_alpha(-255+(self.start_screen_ticks*2))
            self.screen.blit(SPACE_IMG,[0,0])

        if self.level != STARTING_LEVEL and self.stage != LOSE:
            self.dust_overlay()
            self.draw_health_particles()
            y = 30
            for i in range(self.hero.hearts):
                x = 50 * i + 50
                self.screen.blit(HEART_IMG,[x,y])
 
        for sprite in self.all_sprites:
            x = sprite.rect.x - offset_x
            y = sprite.rect.y - offset_y
            self.screen.blit(sprite.image,[x,y])

        # Boss Health
        if self.level != STARTING_LEVEL:
            bosses = self.enemies.sprites()
            self.TheBoss = bosses[0]
            length = 7
            if self.TheBoss.phase != 1 and self.TheBoss.phase != 6:
                pygame.draw.rect(self.screen,[255,255,255],[WIDTH/2-self.TheBoss.hearts*length/4+self.health_x2,HEIGHT - 50+self.health_y2, self.TheBoss.hearts*length/2,8])
                pygame.draw.rect(self.screen,self.COLOR,[WIDTH/2-self.TheBoss.hearts*length/4+self.health_x,HEIGHT - 50+self.health_y, self.TheBoss.hearts/2*length,8])


        #Render Stamina Bar
        pygame.draw.rect(self.screen,[255,255,255],[self.hero.rect.centerx - 20 - offset_x,self.hero.rect.y - 13 - offset_y, 40,5])
                
        if self.hero.dash_cooldown != 0:
            self.destruct = 0.01
        else:
            self.destruct += .04

        self.draw_particles()
        if len(self.spark_particles) > 1:
            self.draw_spark_particles()
        if len(self.red_spark_particles) > 1:
            self.draw_red_spark_particles()
        self.draw_enemy_particles()
        WHITE_IMG.set_alpha(self.win_ticks-50)
        self.screen.blit(WHITE_IMG,[0,0])

        if self.stage != START:
            self.hud.draw(self.screen)
        if self.stage == START:
            pass
        elif self.stage == LEVEL_COMPLETE:
            self.level_complete_screen.draw(self.screen)
        elif self.stage == WIN:
            self.win_screen.draw(self.screen)
            text = FONT_SM.render("You win.", True, BLACK)
            rect = text.get_rect()
            rect.centerx = WIDTH/2
            rect.centery = HEIGHT/2 - 50
            self.screen.blit(text, rect)
            text = FONT_SM.render("Press R to Retry.", True, BLACK)
            rect = text.get_rect()
            rect.centerx = WIDTH/2
            rect.centery = HEIGHT/2+50
            self.screen.blit(text, rect)
        elif self.stage == LOSE:
            for sprite in self.all_sprites:
                x = sprite.rect.x - offset_x
                y = sprite.rect.y - offset_y
                self.screen.blit(sprite.image,[x,y])
            self.debug = True
            self.lose_ticks += 1
            self.lose_screen.draw(self.screen)
            self.screen_shake = 10
            self.hero.dash_cooldown = random.randint(8,13)
            if self.lose_ticks % 200 == 0:
                self.death_count += 1
                print(self.death_count)
                print("Death(s)")
                if self.death_count == 100:
                    print("Achievement unlocked: Time well spent.")
                self.new_game()
            if self.ticks & 20 == 0:
                VIGNETTE.set_alpha(self.lose_ticks/2)
                self.screen.blit(VIGNETTE,[0,0])
            VIGNETTE2.set_alpha(self.lose_ticks/2)
            self.screen.blit(VIGNETTE2,[0,0])
        elif self.stage == PAUSE:
            PAUSE_IMG.set_alpha(160)
            self.screen.blit(PAUSE_IMG,[0,0])
        self.screen.blit(TRANSITION,[self.transition_x,0])
        



        
    def play(self):
        while self.running:
            self.process_input()     
            self.update()     
            self.render()
            self.count_ticks()            
            self.render_offset[0] = self.render_offset[0]
            self.render_offset[1] = self.render_offset[1]
            self.screen.blit(pygame.transform.scale(self.screen,((WIDTH), HEIGHT)),self.render_offset)
            
            
            pygame.display.update()
            self.clock.tick(FPS)


# Let's do this!
if __name__ == "__main__":
   g = Game()
   g.play()
   pygame.quit()   
