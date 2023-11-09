import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, velocity):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = velocity

    def update(self):
        self.rect.y += self.velocity    

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)    