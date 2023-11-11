import pygame
from projectiles.projectile import Projectile

#PROJECTILE_WIDTH = 6
#PROJECTILE_HEIGHT = 12
#PROJECTILE_VELOCITY = 1.5

class Boss:
    def __init__(self, x, y_offscreen, image_path, projectile_img, projectile_group, screen_height, projectile_velocity):
        super().__init__()
        original_image = pygame.image.load(image_path)
        self.width, self.height = 120, 80
        self.image = pygame.transform.scale(original_image, (self.width, self.height)) 
        self.rect = self.image.get_rect(center=(x, y_offscreen))
        self.health = 100
        self.attack_timer = 0
        self.attack_interval = 500
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height - 30)
        self.projectile_img = projectile_img 
        self.projectile_group = projectile_group
        self.screen_height = screen_height
        self.projectile_velocity = projectile_velocity
        self.moving_in = True
        

    def attack(self, player):
        if not self.moving_in:
            projectile_pos = self.rect.midtop
            projectile = Projectile(projectile_pos, self.projectile_img, self.projectile_velocity, 100)
            self.projectile_group.add(projectile)
            self.attack_timer = 0

    def update(self):

        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

        if self.moving_in:
            self.rect.y += 1
            if self.rect.y >= 100:
                self.moving_in = False  

        self.projectile_group.update()    

        for projectile in self.projectile_group:
            if projectile.rect.y > self.screen_height:
                self.projectile_group.remove(projectile)          

    def move_projectiles(self, velocity, player):
        for projectile in self.projectile_group.copy():
            projectile.rect.y += velocity
            if projectile.rect.y > self.screen_height:
                self.projectile_group.remove(projectile)
            elif projectile.rect.colliderect(player.rect):
                self.projectile_group.remove(projectile)
                return True
        return False

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
        for projectile in self.projectile_group:
            projectile.draw(win)

    # def move(self):
    #     self.x += self.velocity


    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0   
    





    