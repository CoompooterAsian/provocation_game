import pygame
import math

from settings import *
from utilities import *


class Entity(pygame.sprite.Sprite):

    def __init__(self, game, image, loc=[0, 0]):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image) 
        self.game = game
        self.rect = self.image.get_rect()

        self.move_to(loc)

        self.on_platform = True

    def move_to(self, loc):
        self.rect.centerx = loc[0] * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = loc[1] * GRID_SIZE + GRID_SIZE // 2

    def apply_gravity(self):
        self.vy += 1
        self.vy = min(self.vy,TERMINAL_VEL)

    def turn_around(self):
        self.vx *= -1

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def move_y_and_check_platforms(self):
        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, self.game.ground, False,pygame.sprite.collide_mask)

        for platform in hits:
            if self.vy > 0:
                self.rect.bottom = platform.rect.top
            elif self.vy < 0:
                self.rect.top = platform.rect.bottom

            self.vy = 0

    def check_world_edges(self):
        at_edge = False

        if self.rect.left < 0:
            self.rect.left = 0
            at_edge = True
        elif self.rect.right > self.game.world_width:
            self.rect.right = self.game.world_width
            at_edge = True

        if at_edge:
            self.turn_around()

    def check_platform_edges(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False,pygame.sprite.collide_mask)
        self.rect.y -= 2

        at_edge = True

        for platform in hits:
            if self.vx > 0:
                if platform.rect.right >= self.rect.right:
                    at_edge = False
            elif self.vx < 0:
                if platform.rect.left <= self.rect.left:
                    at_edge = False

  

    def stop(self):
        if self.vx > self.speed:
            self.vx = self.speed
            self.vx -= 1
        if self.vx < -self.speed:
            self.vx = -self.speed
            self.vx += 1

class Animated_Entity(Entity):

    def __init__(self, game, images, loc=[0, 0]):
        super().__init__(game,images[0],loc)

        self.images = images
        self.game = game
        self.anim_index = 0
        self.ticks = 0
        self.anim_speed = 3

    def set_images_list(self):
        self.images = images

    def run_animation(self):
        self.set_image_list()
        self.ticks += 1
        if self.ticks % self.anim_speed == 0:
            if self.anim_index >= len(self.images):
                self.anim_index = 0
            self.image = self.images[self.anim_index]
            self.anim_index += 1

class Animated_Enemy(Entity):

    def __init__(self, game, images, loc=[0, 0]):
        super().__init__(game,images[0],loc)

        self.images = images
        self.game = game
        self.anim_index = 0
        self.ticks = 0
        self.anim_speed = 3

    def set_images_list(self):
        self.images = images

    def run_animation(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.set_image_list()
        self.ticks += 1
        if self.ticks % self.anim_speed == 0:
            if self.anim_index >= len(self.images):
                self.anim_index = 0
            self.image = self.images[self.anim_index]
            self.anim_index += 1


class Hero(Animated_Entity,Image):

    def __init__(self, game, image):
        super().__init__(game, image)

        self.vx = 0
        self.vy = 0
    
        self.speed = HERO_SPEED
        self.hearts = HERO_HEARTS
        self.dash_cooldown = 0
        self.strike_upgrade = HERO_HASTE
        self.strike_cooldown = 0
        
        self.score = 0
        self.speed_mult = 30

        self.can_dash = True
        self.can_jump = 0
        self.jump_num = 2
        self.anim_speed = 3
        self.direction = 2
        self.still = False
        self.attacktype = 1
        

        self.invincibility_ticks = 0


    def go_left(self):
        self.still = False
        self.direction = 1
        if self.dash_cooldown == 0:
            self.vx = -self.speed
             
    
    def go_right(self):
        self.still = False
        self.direction = 2
        if self.dash_cooldown == 0:
            self.vx = self.speed


    def dash_left(self):
        self.game.swing_sfx.play()
        self.direction = 1
        if self.can_dash == True:
            self.vx = -self.speed *2
            self.game.screen_shake = 10

    def dash_right(self):
        self.game.swing_sfx.play()
        self.direction = 2
        if self.can_dash == True:
            self.vx = self.speed *2
            self.game.screen_shake = 10

    def set_image_list(self):
        if self.direction == 1:
            if len(self.game.attack) != 0 and self.still == True and self.on_platform == True:
                self.images = (HERO_STRIKE_L)
            elif self.on_platform == False and self.dash_cooldown == 0 and self.vy > 0:
                self.images = (HERO_FALL_L)
                self.anim_speed = 3
            elif self.on_platform == False and self.dash_cooldown == 0 and self.vy < 0:
                self.images = (HERO_JUMP_L)
                self.anim_speed = 6
            elif self.on_platform == True and self.dash_cooldown == 0 and self.still == True:
                self.images = (HERO_IDLE_L)
                self.anim_speed = 3
            elif self.on_platform == True and self.dash_cooldown == 0 and self.still == False:
                self.images = (HERO_WALK_L)
                self.anim_speed = 3
            elif self.dash_cooldown != 0:
                self.images = (HERO_DASH_L)
                self.anim_speed = 3
        elif self.direction == 2:
            if len(self.game.attack) != 0 and self.still == True and self.on_platform == True:
                self.images = (HERO_STRIKE_R)
            elif self.on_platform == False and self.dash_cooldown == 0 and self.vy > 0:
                self.images = (HERO_FALL_R)
                self.anim_speed = 3
            elif self.on_platform == False and self.dash_cooldown == 0 and self.vy < 0:
                self.images = (HERO_JUMP_R)
                self.anim_speed = 6
            elif self.on_platform == True and self.dash_cooldown == 0 and self.still == True:
                self.images = (HERO_IDLE_R)
                self.anim_speed = 3
            elif self.on_platform == True and self.dash_cooldown == 0 and self.still == False:
                self.images = (HERO_WALK_R)
                self.anim_speed = 3
            elif self.dash_cooldown != 0:
                self.images = (HERO_DASH_R)
                self.anim_speed = 3
        

    def gravity(self):
        if self.dash_cooldown == 0:
            self.vy += 1 + self.game.jump_boost/10
            self.vy = min(self.vy,TERMINAL_VEL+self.game.jump_boost/5)
        else:
            self.vy = 0

    def move_check_platforms(self):
        self.rect.centerx += self.vx
        
        collide = pygame.sprite.spritecollide(self,self.game.platforms,False,pygame.sprite.collide_mask)
        for platform in collide:
            if self.vx > 0:
                self.rect.right = platform.rect.left + 30
            elif self.vx < 0:
                self.rect.left = platform.rect.right - 30
            self.dash_cooldown = 0

        self.rect.centery += self.vy
        self.on_platform = False
        
        collide = pygame.sprite.spritecollide(self,self.game.platforms,False,pygame.sprite.collide_mask) or pygame.sprite.spritecollide(self,self.game.ground,False,pygame.sprite.collide_mask)
        for platform in collide:
            if self.vy > 0:
                self.rect.bottom = platform.rect.top 
                self.on_platform = True
                self.can_dash = True
                self.can_jump = 0
            elif self.vy < 0:
                self.rect.top = platform.rect.bottom
            self.vy = 0

    def create_particles(self):
        offset_x,offset_y = self.game.get_offsets()
        self.game.particles.append([[self.rect.centerx - offset_x,self.rect.centery - offset_y+8],[random.randint(0,20)/10 -1, random.randint(0,30)/10 - 1.5], self.dash_cooldown/2])

    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.game.world_width:
            self.rect.right = self.game.world_width

    def stop(self):
        if self.vx > 0:
            if self.vx > self.speed:
                self.vx = self.speed
            self.vx -= 1
        elif self.vx < 0:
            if self.vx < -self.speed:
                self.vx = -self.speed
            self.vx += 1

        self.still = True
        
    def jump(self):
        if self.can_jump < (self.jump_num):
            self.anim_index = -1
            self.anim_speed = 10
            self.vy = -HERO_JUMP_POWER - self.game.jump_boost
            self.can_jump += 1

    def attack(self):
        self.game.swing_sfx.play()
        self.strike_cooldown = self.strike_upgrade
        if self.attacktype == 1:
            self.attacktype = 2
        else:
            self.attacktype = 1
        if self.direction == 1:
            slash = Slash(self.game,Image(SLASH[0]).flip_x(),self.rect.midleft,-100,self.attacktype)
        elif self.direction == 2:
            slash = Slash(self.game,Image(SLASH[0]),self.rect.midright,100,self.attacktype)
        self.game.attack.add(slash)
        self.game.all_sprites.add(slash)

    def check_enemies(self):
        if self.invincibility_ticks < 5:
            self.image.set_alpha(255)
        else:
            if self.invincibility_ticks % 5 == 0:
                self.image.set_alpha(100)
            if self.invincibility_ticks % 10 == 0:
                self.image.set_alpha(200)

        if self.invincibility_ticks == 0:
            for boss in self.game.enemies:
                if boss.vulnerable == True:
                    hits = pygame.sprite.spritecollide(self,self.game.enemies,False,pygame.sprite.collide_mask)

                    for enemy in hits:
                        self.hearts -= 1
                        self.game.spark_particles.append([[self.rect.centerx,self.rect.centery],[random.randint(0,100)/10 -5, random.randint(-30,15)/10 - 1.5], 4])
                        self.game.spark_particles.append([[self.rect.centerx,self.rect.centery],[random.randint(0,100)/10 -5, random.randint(-30,15)/10 - 1.5], 5])
                        self.game.spark_particles.append([[self.rect.centerx,self.rect.centery],[random.randint(0,100)/10 -5, random.randint(-30,15)/10 - 1.5], 6])
                        self.invincibility_ticks = 60

                        self.game.screen_shake = 25
            
        else:
            self.invincibility_ticks -= 1

        if self.hearts <= 0:
            self.image.set_alpha(255)
            self.images = HERO_DEATH
            self.set_image_list()
            self.run_animation()
            self.game.lose()
            self.game.death1_sfx.play()
            self.game.death2_sfx.play()

    def check_statue(self):
        hits = pygame.sprite.spritecollide(self,self.game.statue,False,pygame.sprite.collide_mask)
        for statue in hits:
            self.game.transition = True
        if self.game.transition_x > -1000:
            if self.game.level == 1:
                self.game.advance()               
            
            
    def update(self):
        self.check_enemies()
        self.create_particles()
        self.set_image_list()
        self.run_animation()
        self.gravity()
        self.check_world_edges()
        self.move_check_platforms()
        self.check_statue()
        
# Attack
class Slash(Entity,Image):
    def __init__(self, game, image,loc,x_adj,y_adj):
        super().__init__(game, image)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.anim_index = 0
        self.x,self.y = loc
        self.x_adj,self.y_adj = x_adj,y_adj
        for hero in self.game.player:
            if hero.direction == 1:
                self.direction = 1
            elif hero.direction == 2:
                self.direction = 2

    def run_animation(self):
        self.rect.centerx = self.game.hero.rect.centerx + self.x_adj
        self.rect.centery = self.game.hero.rect.centery
        if self.game.ticks & HERO_STRIKE_SPEED == 0:
            self.anim_index += 1
            if self.anim_index >= len(SLASH):
                self.anim_index = 0
                self.kill()
            for hero in self.game.player:
                if self.direction == 1:
                    if hero.attacktype == 1:
                        self.image = Image(SLASH[self.anim_index]).flip_x()
                    else:
                        self.image = Image(SLASH[self.anim_index]).flip_x_y()
                elif self.direction == 2:
                    self.image = Image(SLASH[self.anim_index])
                    if hero.attacktype == 1:
                        self.image = Image(SLASH[self.anim_index])
                    else:
                        self.image = Image(SLASH[self.anim_index]).flip_y()
        if self.game.hero.hearts <= 0:
            self.kill()
            
    def update(self):
        self.run_animation()


# Enemies:
class Boss(Animated_Enemy):
        
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

        self.vx = 0
        self.speed = 10
        self.vy = 0
        self.hearts = BOSS_HEARTS

        self.phase = 1
        
        self.vulnerable = True
        self.win_ticks = 0
        self.right = False

    def move(self):
        self.rect.x += self.vx

    def set_image_list(self):
        if self.phase == 1:
            self.anim_speed = 180
            self.images = BOSS_SCREECH

    def check_hits(self):
        offset_x,offset_y = self.game.get_offsets()
        self.image.set_alpha(255)
        self.game.COLOR = [150,0,0]
        self.game.health_x = 0
        self.game.health_y = 0
        self.game.health_x2 = 0
        self.game.health_y2 = 0
        collide = pygame.sprite.spritecollide(self,self.game.attack,False,pygame.sprite.collide_mask)
        for attack in collide:
            self.hearts -= 1
            self.game.red_spark_particles.append([[self.rect.centerx,self.rect.centery],[random.randint(0,100)/10 -5, random.randint(-30,15)/10 - 1.5], random.randint(5,7)])
            self.image.set_alpha(150)
            self.game.COLOR = [255,60,60]
            self.game.health_x = random.randrange(-100,100)
            self.game.health_y = random.randrange(-12,12)
            self.game.health_x2 = random.randrange(-100,100)
            self.game.health_y2 = random.randrange(-12,12)
            
            if self.rect.centerx < self.game.hero.rect.centerx:
                self.game.hero.vx = 20
            elif self.rect.centerx > self.game.hero.rect.centerx:
                self.game.hero.vx = -20
                

            self.game.screen_shake = 5

            if self.phase == 1:
                
                self.game.fighting = True
                self.phase = 6

            if self.hearts == 0:
                self.game.fighting = False
                self.anim_index = 0
                self.game.swing_sfx.stop()
                self.game.dash_sfx.stop()
                self.game.screech_sfx.play()
                self.game.death2_sfx.play()
                self.game.death1_sfx.play()

    def set_image_list(self):
        if self.hearts <= 0:
            self.vx = 0
            self.game.win_ticks += 1
            offset_x,offset_y = self.game.get_offsets()
            self.anim_speed = 5
            self.images = BOSS_DEATH
            self.vulnerable = False
            if self.game.win_ticks < 250:
                self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery - offset_y],[random.randint(0,1000)/10 - 50, random.randint(0,100)/10 -5], random.randint(5,15)])
                self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery - offset_y],[random.randint(0,2000)/10 -100, random.randint(0,2000)/10 -100], random.randint(5,15)])
                self.anim_index = 0
            self.game.screen_shake = 40
            if self.anim_index >= len(self.images)-1:
                self.game.win()

    def scream(self):
        offset_x,offset_y = self.game.get_offsets()
        self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery - offset_y],[random.randint(0,2000)/10 -100, random.randint(0,2000)/10 -100], random.randint(5,15)])
        self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery - offset_y],[random.randint(0,2000)/10 -100, random.randint(0,2000)/10 -100], random.randint(5,15)])
        self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery - offset_y],[random.randint(0,2000)/10 -100, random.randint(0,2000)/10 -100], random.randint(5,15)])
        self.game.screen_shake = 100
        self.anim_speed = 1
        self.images = BOSS_SCREECH
        if self.anim_index == 5:
            self.game.screech_sfx.play()
        if self.anim_index > 5:
            self.anim_speed = 15
        if self.anim_index == len(self.images)-1:
            self.anim_speed = 1
        if self.anim_index >= len(self.images):
            self.choose_attack()

    def check_direction(self):
        if self.game.hero.rect.centerx < self.rect.centerx:
            self.right = False
        elif self.game.hero.rect.centerx > self.rect.centerx:
            self.right = True

    def choose_attack(self):
        distance = abs(self.rect.centerx-self.game.hero.rect.centerx)
        if self.anim_index >= len(self.images):
            self.check_direction()
            if distance < 230:
                if self.game.hero.rect.centery < self.rect.centery:
                    self.phase = 2
                else:
                    self.phase = 3
            elif 229 < distance < 800:
                r = [5,2,2]
                self.phase = random.choice(r)
            else:
                self.phase = 4
            self.anim_index = 0

    def attack_1(self):
        if self.right == False:
            self.images = BOSS_WALK_R
        elif self.right == True:
            self.images = BOSS_WALK_L
        if 10 < self.anim_index < 20:
            self.anim_speed = 1
            if self.anim_index == 11:
                self.game.swing_sfx.stop()
                self.game.swing_sfx.play()
            if self.right == False:
                self.vx = -45
            elif self.right == True:
                self.vx = 45
        elif 19 < self.anim_index < len(self.images)-1:
            self.vx = 0
            self.anim_speed = 3
        else:
            self.anim_speed = 2
        if self.anim_index >= len(self.images):
            self.choose_attack()

    def attack_2(self):
        self.anim_speed = 2
        if self.phase == 3 and self.right == False:
            self.images = BOSS_PUNCH_R
        elif self.phase == 3 and self.right == True:
            self.images = BOSS_PUNCH_L
        if self.anim_index > 13:
            self.anim_speed = 1
        if self.anim_index >= len(self.images):
            self.choose_attack()

    def attack_3(self):
        if self.right == False:
            self.images = BOSS_WALK_R
        elif self.right == True:
            self.images = BOSS_WALK_L
        if -1 < self.anim_index < 11:
            self.anim_speed = 6
        elif 10 < self.anim_index < 20:
            self.anim_speed = 2
            if self.anim_index == 11:
                self.game.dash_sfx.stop()
                self.game.dash_sfx.play()
            if self.anim_index == 15:
                self.game.screen_shake = 30
            if self.right == False:
                self.vx = -80
            elif self.right == True:
                self.vx = 80
        elif self.anim_index < 23:
            self.vx = 0
            self.anim_speed = 15
        else:
            self.anim_speed = 1
        if self.anim_index >= len(self.images):
            self.choose_attack()

    def attack_4(self):
        if self.right == False:
            self.images = BOSS_AIR_R
        elif self.right == True:
            self.images = BOSS_AIR_L

        if -1 < self.anim_index < 7:
            if self.anim_index == 0:
                self.game.airboom_sfx.stop()
                self.game.airboom_sfx.play()
            self.anim_speed = 7
        elif 6 < self.anim_index < 10:
            self.anim_speed = 2
            self.rect.y -= 50
            if self.right == True:
                self.rect.x += 50
            else:
                self.rect.x += -50
        elif 9 < self.anim_index < 13:
            if self.anim_index == 10:
                self.check_direction()
            self.anim_speed = 10
            self.rect.y -= 25
            if self.right == False:
                self.images = BOSS_AIR_R
            elif self.right == True:
                self.images = BOSS_AIR_L
        elif 12 < self.anim_index < 19:
            self.anim_speed = 1
            self.rect.y += 50
            if self.right == True:
                self.rect.x += 50
            else:
                self.rect.x += -50
            if self.anim_index > 16:
                if self.anim_index == 17:
                    self.game.airboom_sfx.fadeout(400)
                    self.game.screen_shake = 30
                offset_x,offset_y = self.game.get_offsets()
                self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery + 200],[random.randint(0,1000)/10 - 50, random.randint(0,100)/10 -5], random.randint(5,15)])
                self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery + 200],[random.randint(0,1000)/10 - 50, random.randint(0,100)/10 -5], random.randint(5,15)])
                self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery + 200],[random.randint(0,1000)/10 - 50, random.randint(0,100)/10 -5], random.randint(5,15)])
                self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery + 200],[random.randint(0,1000)/10 - 50, random.randint(0,100)/10 -5], random.randint(5,15)])
                self.game.enemy_particles.append([[self.rect.centerx,self.rect.centery + 200],[random.randint(0,1000)/10 - 50, random.randint(0,100)/10 -5], random.randint(5,15)])

        elif self.anim_index < len(self.images)+1:
            self.anim_speed = 18

        else:
            self.anim_speed = 1
            
        if self.anim_index >= len(self.images):
            self.choose_attack()
        

    def update(self):
        self.set_image_list()
        self.run_animation()
        self.move()
        if not self.hearts <= 0:
            self.apply_gravity()
            self.move_y_and_check_platforms()
        self.check_platform_edges()
        self.check_world_edges()
        self.check_hits()
        self.stop()
        if not self.hearts <= 0:
            if self.phase == 2:
                self.attack_1()
            elif self.phase == 3:
                self.attack_2()
            elif self.phase == 4:
                self.attack_3()
            elif self.phase == 5:
                self.attack_4()
            elif self.phase == 6:
                self.scream()

        


class Dummy(Animated_Enemy):
        
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

    def check_hits(self):
        offset_x,offset_y = self.game.get_offsets()
        self.image.set_alpha(255)
        collide = pygame.sprite.spritecollide(self,self.game.attack,False,pygame.sprite.collide_mask)
        for attack in collide:
            self.game.spark_particles.append([[self.rect.centerx,self.rect.centery - offset_y+8],[random.randint(0,100)/10 -5, random.randint(-30,15)/10 - 1.5], 3])
            self.game.points += 1
            self.run_animation()
            self.image.set_alpha(150)
            if self.rect.centerx < self.game.hero.rect.centerx:
                self.game.hero.vx = 20
            elif self.rect.centerx > self.game.hero.rect.centerx:
                self.game.hero.vx = -20
                
    def set_image_list(self):
        self.images = DUMMY

    def update(self):
        self.set_image_list()
        self.check_hits()


class Statue(Animated_Enemy):
        
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

        
#Tiles
class Platform(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

        
# Items
class Gem:

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

    def apply(self, character):
        pass


