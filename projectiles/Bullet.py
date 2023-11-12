import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, image, velocity, hitbox_reduction):
        super().__init__()
        self.image = image
        self.velocity = velocity
        hitbox_reduction = hitbox_reduction

        self.rect = self.image.get_rect(center=pos)

        # Dynamically adjust the rect size for the hitbox
        hitbox_width = max(self.rect.width - hitbox_reduction, 1)  
        hitbox_height = max(self.rect.height - hitbox_reduction, 1)
        self.rect.size = (hitbox_width, hitbox_height)
        self.rect.center = pos  

    def update(self):
        self.rect.y -= self.velocity
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, window):
        
        image_x = self.rect.centerx - self.image.get_width() // 2
        image_y = self.rect.centery - self.image.get_height() // 2

        window.blit(self.image, (image_x, image_y))

        # Draw the hitbox for debugging
        #pygame.draw.rect(window, (255, 0, 0), self.rect, 1)

