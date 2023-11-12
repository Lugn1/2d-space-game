import pygame
from projectiles.projectile import Projectile


pygame.init()
# TODO change this to a enemy projectile sound
default_projectile_sound = pygame.mixer.Sound("./sound_effects/bulletDefaultSound.wav")


class Enemy:
    # x, y, img, projectile_img, projectile_width, projectile_height, projectile_velocity, projectiles[], velocity, width, height TODO maybe change to this
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
        if not self.movement_pattern:
            self.y += self.velocity
            self.rect.y = self.y
        else: 
            if self.rect.y >= 100:
                self.movement_pattern.move(self)
            else:
                self.y += self.velocity
                self.rect.y = self.y
                
        self.x = self.rect.x
        self.y = self.rect.y



    def draw(self, win):
        if self.type == 'enemy1':
            win.blit(self.img, (self.x, self.y))
             #pygame.draw.rect(WIN, "red", enemy, 2)
        elif self.type == 'enemy2':
             win.blit(self.img, (self.x, self.y))




    def shoot(self):
        if self.shoot_count == 200:
            if self.type == 'enemy1':
                #projectile_sound.play()
                projectile_pos = self.rect.midtop
            if self.type == 'enemy2':
                #projectile_sound.play()
                projectile_pos = (self.rect.x + self.width // 2, self.rect.y)
            
            
            projectile = Projectile(projectile_pos, self.projectile_img, self.projectile_velocity, 60) #pygame.Rect(projectile_x, projectile_y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
            self.projectiles.append(projectile)
            self.shoot_count = 0
        self.shoot_count += 1    
            