import pygame
from projectiles.projectile import Projectile

pygame.init()
projectile_sound = pygame.mixer.Sound("./sound_effects/bulletDefaultSound.wav")


ENEMY_WIDTH = 45
ENEMY_HEIGHT = 30 
PROJECTILE_WIDTH = 6
PROJECTILE_HEIGHT = 12
PROJECTILE_VELOCITY = 3
projectiles = []
ENEMY_VELOCITY = 2

class Enemy:
    def __init__(self, x, y, img, projectile_img, projectiles, velocity):
        self.x = x
        self.y = y
        self.img = img
        self.shoot_count = 0
        self.projectile_img = projectile_img
        self.projectiles = projectiles
        self.velocity = velocity
        self.rect = pygame.Rect(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT)

    def move(self):
        self.y += self.velocity
        self.rect.y = self.y

    def shoot(self):
        if self.shoot_count == 200:
            #projectile_sound.play()
            projectile_pos = self.rect.midtop
            projectile = Projectile(projectile_pos, self.projectile_img, PROJECTILE_VELOCITY, 60) #pygame.Rect(projectile_x, projectile_y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
            self.projectiles.append(projectile)
            self.shoot_count = 0
        self.shoot_count += 1    
            