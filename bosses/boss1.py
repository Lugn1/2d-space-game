import pygame



class Boss:
    def __init__(self, x, y, image_path, projectiles):
        original_image = pygame.image.load(image_path)
        self.width, self.height = 120, 80
        self.image = pygame.transform.scale(original_image, (self.width, self.height)) 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.attack_timer = 0
        self.attack_interval = 500
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height - 30)
        self.projectiles = projectiles
        

    def attack(self, player):
        projectile = pygame.Rect(self.rect.x + self.width // 2, self.rect.y + self.height, 6, 12)
        self.projectiles.append(projectile)
        self.attack_timer = 0

    def move_projectiles(self, velocity, player):
        for projectile in self.projectiles[:]:
            projectile.y += velocity
            if projectile.y > 800:
                self.projectiles.remove(projectile)
            elif projectile.colliderect(player):
                self.projectiles.remove(projectile)
                return True
        return False

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
        for projectile in self.projectiles:
            pygame.draw.rect(win, (255, 0, 0), projectile)

    def move(self):
        self.x += self.velocity


    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0   
    





    