import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, image, velocity):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.velocity = velocity


    def update(self):
        self.rect.y -= self.velocity
        if self.rect.bottom < 0:
            self.kill()


    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

