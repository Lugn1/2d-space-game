import pygame

ENEMY_WIDTH = 45
ENEMY_HEIGHT = 30 
PROJECTILE_WIDTH = 6
PROJECTILE_HEIGHT = 12
PROJECTILE_VELOCITY = 3
projectiles = []
ENEMY_VELOCITY = 2

class Enemy:
    def __init__(self, x, y, img, projectiles, velocity):
        self.x = x
        self.y = y
        self.img = img
        self.shoot_count = 0
        self.projectiles = projectiles
        self.velocity = velocity
        self.rect = pygame.Rect(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT)

    def move(self):
        self.y += self.velocity
        self.rect.y = self.y

    def shoot(self):
        if self.shoot_count == 200:
            projectile_x = self.x + ENEMY_WIDTH / 2 - PROJECTILE_WIDTH / 2
            projectile_y = self.y + 20
            projectile = pygame.Rect(projectile_x, projectile_y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
            self.projectiles.append(projectile)
            self.shoot_count = 0
        self.shoot_count += 1    
            