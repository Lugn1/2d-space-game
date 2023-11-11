import pygame
from projectiles.bullet import Bullet

pygame.init()
bullet_sound = pygame.mixer.Sound("./sound_effects/bulletDefaultSound.wav")
class Player:
    def __init__(self, x, y, image, width, height, velocity, screen_height, screen_width, bullet_velocity, bullet_width, bullet_height):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = width
        self.height = height
        self.velocity = velocity
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.bullet_velocity = bullet_velocity
        self.bullet_height = bullet_height
        self.bullet_width = bullet_width
        self.bullet_cooldown = 500
        self.last_shot = pygame.time.get_ticks()
        # add dash
        self.dash_velocity = self.velocity * 3
        self.dash_duration = 10
        self.dash_cooldown = 400
        self.is_dashing = False
        self.dash_timer = 0


    def move(self, keys):

        # add dash
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            if not self.is_dashing and self.dash_timer == 0:
                self.is_dashing = True
                self.dash_timer = self.dash_duration

        # current speed bases on dash or not
        current_velocity = self.dash_velocity if self.is_dashing else self.velocity        

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.rect.x = max(0, self.rect.x - current_velocity)      
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.rect.x = min(self.screen_width - self.width, self.rect.x + current_velocity)
        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            self.rect.y = max(0, self.rect.y - current_velocity) 
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.rect.y = min(self.screen_height - self.height, self.rect.y + current_velocity)
        
        # dash timer
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                # start cooldown
                self.dash_timer = -self.dash_cooldown
        
        # cooldown recovery
        if self.dash_timer < 0:
            self.dash_timer += 1
            print("Cooldown: ", self.dash_timer)

    def shoot(self, bullet_group, bullet_image):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.bullet_cooldown:
            bullet_sound.play()
            bullet_pos = self.rect.midtop
            bullet_velocity = self.bullet_velocity
            # Send bullet hitbox size as an argument to match the hitbox for later when 
            # multiple bullets are being used
            bullet = Bullet(bullet_pos, bullet_image, bullet_velocity, 90)
            bullet_group.add(bullet)
            self.last_shot = current_time


    def draw(self, window):
        window.blit(self.image, self.rect)           