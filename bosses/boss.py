import pygame
import random
from projectiles.projectile import Projectile
from projectiles.zigzag_projectile import ZigzagProjectile
from utils.resourcePath import resource_path

class Boss:
    def __init__(self, x, y_offscreen, projectile_img, projectile_group, screen_width, screen_height, projectile_velocity, movement_pattern, health):
        super().__init__()
        original_image = pygame.image.load(resource_path("./sprites/boss1.png"))
        self.width, self.height = 120, 80
        self.image = pygame.transform.scale(original_image, (self.width, self.height)) 
        self.rect = self.image.get_rect(center=(x, y_offscreen))
        self.max_health = health
        self.current_health = self.max_health
        self.attack_timer = 0
        self.attack_interval = 500
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height - 30)
        self.projectile_img = projectile_img 
        self.projectile_group = projectile_group
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.projectile_velocity = projectile_velocity
        self.moving_in = True
        self.movement_pattern = movement_pattern
        # change health depending on what boss
        self.health_bar_width = self.max_health * 5
        self.health_bar_height = 20
        self.health_bar_x = screen_width / 2 - self.health_bar_width / 2
        self.health_bar_y = 10
        self.health_bar_color = (255, 0, 0)

    def attack(self, player):
        if not self.moving_in:
            projectile_type = random.choice(['default', 'zigzag'])
            if projectile_type == 'normal':
                projectile = Projectile(self.rect.midtop, self.projectile_img, self.projectile_velocity, 100)
            elif projectile_type == 'zigzag':
                projectile = ZigzagProjectile(self.rect.midtop, self.projectile_img, self.projectile_velocity - 2.5, 100, amplitude=5, frequency=50)
            else:
                projectile = Projectile(self.rect.midtop, self.projectile_img, self.projectile_velocity, 100)
            
            self.projectile_group.add(projectile)
            self.attack_timer = 0

    def update(self):
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

        if self.moving_in:
            self.rect.y += 1
            if self.rect.y >= 100:
                self.moving_in = False  

        if not self.moving_in:
            self.projectile_group.update()    
            self.movement_pattern.move(self)
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

    def draw_health_bar(self, screen):
        border_color = (0, 0, 0)  
        border_thickness = 4
    
        current_bar_width = (self.current_health / self.max_health) * self.health_bar_width
        
        # draw border
        pygame.draw.rect(screen, border_color, [self.health_bar_x - border_thickness, self.health_bar_y - border_thickness, self.health_bar_width + 2 * border_thickness, self.health_bar_height + 2 * border_thickness])
        # draw background for the hp bar
        pygame.draw.rect(screen, (128, 128, 128), [self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height])
        # draw current health
        pygame.draw.rect(screen, self.health_bar_color, [self.health_bar_x, self.health_bar_y, current_bar_width, self.health_bar_height])

        # Draw the hitbox for debugging
        #pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)

    # def move(self):
    #     self.x += self.velocity


    def take_damage(self, damage):
        self.current_health -= damage
        self.current_health = max(self.current_health, 0)
        return self.current_health <= 0
        #self.health -= damage
        #return self.health <= 0   


    def get_health_percentage(self):
        return (self.current_health/self.max_health) * 100    
    





    