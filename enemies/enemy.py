import pygame
from projectiles.projectile import Projectile
from utils.resourcePath import resource_path

pygame.init()
# TODO change this to a enemy projectile sound
default_projectile_sound = pygame.mixer.Sound(resource_path("./sound_effects/bulletDefaultSound.wav"))


class Enemy:
    # x, y, img, projectile_img, projectile_width, projectile_height, projectile_velocity, projectiles[], velocity, width, height, type, move_pattern TODO maybe change to this
    def __init__(self, x, y, img, projectile_img, projectiles, projectile_velocity, velocity, width, height, type, movement_pattern=None):
        self.x = x
        self.y = y
        self.img = img 
        self.projectile_img = projectile_img
        self.projectiles = projectiles
        self.projectile_velocity = projectile_velocity
        self.velocity = velocity
        self.width = width
        self.height = height
        self.type = type
        self.movement_pattern = movement_pattern
        
        self.shoot_count = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        if self.type == 'enemy1':
            self.y += self.velocity
            self.rect.y = self.y
        elif self.type == 'enemy2':
            if self.rect.y >= 100:
                self.movement_pattern.move(self)
            else:
                self.y += self.velocity
                self.rect.y = self.y
        elif self.type == 'enemy3':
            self.movement_pattern.move(self)
            self.y += self.velocity
            self.rect.y = self.y            
        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self, win):
        if self.type == 'enemy1':
            win.blit(self.img, (self.x, self.y))
            # draw for debug 
            #pygame.draw.rect(win, "red", self, 2)
        elif self.type == 'enemy2':
            win.blit(self.img, (self.x, self.y))
            # draw for debug
            #pygame.draw.rect(win, "red", self, 2)
        elif self.type == 'enemy3':
            win.blit(self.img, (self.x, self.y))
            # draw for debug
            #pygame.draw.rect(win, "green", self, 2)     

    def shoot(self):
        shoot_threshold_enemy1 = 150
        shoot_threshold_enemy2 = 40
        shoot_threshold_enemy3 = 80

        if self.type == 'enemy1':
            if self.shoot_count >= shoot_threshold_enemy1:
                #projectile_sound.play()
                projectile_pos = self.rect.midtop
                self.reset_shoot_count(projectile_pos)
        elif self.type == 'enemy2':
            if self.shoot_count >= shoot_threshold_enemy2:
                #projectile_sound.play()
                projectile_pos = (self.rect.x + self.width // 2, self.rect.y)
                self.reset_shoot_count(projectile_pos)   
        elif self.type == 'enemy3':
            if self.shoot_count >= shoot_threshold_enemy3:
                projectile_pos = self.rect.midtop
                self.reset_shoot_count(projectile_pos)         
        self.shoot_count += 1 

    def reset_shoot_count(self, projectile_pos):
        projectile = Projectile(projectile_pos, self.projectile_img, self.projectile_velocity, 60) #pygame.Rect(projectile_x, projectile_y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
        self.projectiles.append(projectile)
        self.shoot_count = 0           
            