import pygame

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))


    def move(self, keys):
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.rect.x = max(0, self.rect.x - PLAYER_VELOCITY)      
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.rect.x = min(WIDTH - self.rect.width, self.rect.x + PLAYER_VELOCITY)
        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            self.rect.y = max(0, self.rect.y - PLAYER_VELOCITY) 
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.rect.y = min(HEIGHT - PLAYER_HEIGHT, self.rect.y + PLAYER_VELOCITY) 