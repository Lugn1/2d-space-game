import pygame

class Player:
    def __init__(self, x, y, image, width, height, velocity, screen_height, screen_width, bullet_width, bullet_height):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = width
        self.height = height
        self.velocity = velocity
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.bullet_height = bullet_height
        self.bullet_width = bullet_width
        self.bullet_cooldown = 500
        self.last_shot = pygame.time.get_ticks()


    def move(self, keys):
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.rect.x = max(0, self.rect.x - self.velocity)      
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.rect.x = min(self.screen_width - self.width, self.rect.x + self.velocity)
        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            self.rect.y = max(0, self.rect.y - self.velocity) 
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.rect.y = min(self.screen_height - self.height, self.rect.y + self.velocity) 

    def shoot(self, bullets, bullet_image):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.bullet_cooldown:
            left_offset = 20
            top_offset = 20
            print(bullet_image.get_size())
            bullet = pygame.Rect(
                self.rect.centerx - (self.bullet_width // 2) - left_offset, 
                self.rect.top - (self.bullet_height // 2) - top_offset,
                self.bullet_width, self.bullet_height
                )
            bullets.append((bullet, bullet_image))
            self.last_shot = current_time


    def draw(self, window):
        window.blit(self.image, self.rect)           