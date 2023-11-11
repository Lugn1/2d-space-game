import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, image, velocity, hitbox_reduction):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(pos))
        self.velocity = velocity
        self.hitbox_reduction = hitbox_reduction

        self.rect = self.image.get_rect(center=(pos[0], pos[1] + 20))

        # Dynamically adjust the rect size for the hitbox
        hitbox_width = max(self.rect.width - hitbox_reduction, 1)  
        hitbox_height = max(self.rect.height - hitbox_reduction, 1)
        self.rect.size = (hitbox_width, hitbox_height)
        self.rect.center = center=(pos[0], pos[1] + 20)  

    def update(self):
        self.rect.y += self.velocity    

    def draw(self, win):
          
        image_x = self.rect.centerx - self.image.get_width() // 2
        image_y = self.rect.centery - self.image.get_height() // 2 + 2
        
        win.blit(self.image, (image_x, image_y)) 

        # Draw the hitbox for debugging
        pygame.draw.rect(win, (0, 255, 0), self.rect, 1)