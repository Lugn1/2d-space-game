import pygame
import math
from projectiles.bullet import Bullet
from utils.resourcePath import resource_path

pygame.init()
bullet_sound = pygame.mixer.Sound(resource_path("./sound_effects/bulletDefaultSound.wav"))
dash_sound = pygame.mixer.Sound(resource_path("./sound_effects/player_dash.wav"))
class Player:
    def __init__(self, x, y, image, width, height, velocity, screen_height, screen_width, bullet_velocity, bullet_width, bullet_height):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.lives = 3
        self.current_hp = self.lives
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
        self.dash_velocity = self.velocity * 2
        self.dash_duration = 10
        self.dash_cooldown = 400
        self.is_dashing = False
        self.dash_timer = 0
        # dash tracker for visual
        self.dash_tracker_width = self.width
        self.dash_tracker_height = 5
        self.dash_tracker_x = 20
        self.dash_tracker_y = self.screen_height - 30
        self.dash_tracker_color = (40, 200, 255)
        # movement tracker and speed-up
        self.is_moving_horizontally = False
        self.horizontal_move_start_time = None
        self.horizontal_velocity_increase = 0
        
        self.game_over = False


    def move(self, keys):
        moving_horizontally = (keys[pygame.K_a] or keys[pygame.K_LEFT]) or (keys[pygame.K_d] or keys[pygame.K_RIGHT])
        moving_vertically = (keys[pygame.K_w] or keys[pygame.K_UP]) or (keys[pygame.K_s] or keys[pygame.K_DOWN])

        is_diagonal = moving_horizontally and moving_vertically

        if moving_horizontally and not self.is_moving_horizontally:
            self.is_moving_horizontally = True
            self.horizontal_move_start_time = pygame.time.get_ticks()

        if not moving_horizontally and self.is_moving_horizontally:
            # Stopped moving horizontally
            self.is_moving_horizontally = False
            self.horizontal_velocity_increase = 0  # Reset velocity increase
        
        # Check for sustained horizontal movement
        if self.is_moving_horizontally:
            if pygame.time.get_ticks() - self.horizontal_move_start_time > 1000:  # 1 second
                # Increase velocity by a certain amount, could also implement a max limit here
                self.horizontal_velocity_increase = min(self.horizontal_velocity_increase + 0.5, 5)  # Example increment and max limit

        if moving_horizontally:
            self.velocity += self.horizontal_velocity_increase  # Adjust velocity based on sustained movement            

        # add dash
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            if not self.is_dashing and self.dash_timer == 0:
                
                self.is_dashing = True
                self.dash_timer = self.dash_duration
        # current speed bases on dash or not
        current_velocity = self.dash_velocity if self.is_dashing else self.velocity  
        # Adjust speed for diagonal movement 
        if is_diagonal:
            current_velocity /= math.sqrt(2)
    
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.rect.x = max(0, self.rect.x - current_velocity)
            #self.rect.x = max(0, self.rect.x - current_velocity)      
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.rect.x = min(self.screen_width - self.width, self.rect.x + current_velocity)
            #self.rect.x = min(self.screen_width - self.width, self.rect.x + current_velocity)
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
            #print("Cooldown: ", self.dash_timer)


    def shoot(self, bullet_group, bullet_image):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.bullet_cooldown:
            bullet_sound.play()
            bullet_pos = self.rect.midtop
            bullet_velocity = self.bullet_velocity
            # Send bullet hitbox size as an argument to match the hitbox for later when 
            # multiple bullets are being used
            bullet = Bullet(bullet_pos, bullet_image, bullet_velocity, 110)
            bullet_group.add(bullet)
            self.last_shot = current_time

            
    def is_hit(self):
        print(self.current_hp)
        self.current_hp -= 1
        if self.current_hp <= 0:
            self.game_over = True
        return self.current_hp <= 0
        

    def draw(self, window):
        window.blit(self.image, self.rect)   
        # Draw the hitbox for debugging
        #pygame.draw.rect(window, (0, 255, 0), self.rect, 1)        


    def draw_dash_tracker(self, screen):

        tracker_x = self.rect.x + self.width / 2 - self.dash_tracker_width / 2
        tracker_y = self.rect.y + self.height + 5

        if self.dash_timer < 0:
            filled_width = max(0, (self.dash_cooldown + self.dash_timer) / self.dash_cooldown * self.dash_tracker_width)  
            pygame.draw.rect(screen, self.dash_tracker_color, (tracker_x, tracker_y, filled_width, self.dash_tracker_height)) 