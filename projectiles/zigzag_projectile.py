from projectiles.projectile import Projectile
import random


class ZigzagProjectile(Projectile):
    def __init__(self, pos, image, velocity, hitbox_reduction, amplitude, frequency):
        super().__init__(pos, image, velocity, hitbox_reduction)
        self.amplitude = amplitude
        self.frequency = frequency
        self.tick_counter = 0
        self.hitbox_reduction = hitbox_reduction
        self.direction = random.choice([-1, 1])
        self.switch_direction_tick = frequency
    

    def update(self):
        super().update()
        if self.tick_counter >= self.switch_direction_tick:
            self.direction *= -1
            self.switch_direction_tick += self.frequency
            print(f"Direction changed to {self.direction}")  # Debugging print
        
        self.rect.x += self.amplitude * self.direction
        self.tick_counter += 1        
        print(f"Tick: {self.tick_counter}, X: {self.rect.x}")  # Debugging print