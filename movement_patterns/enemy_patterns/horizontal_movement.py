from movement_patterns.movement_pattern import MovementPattern
import random

class EnemyHorizontalMovementPattern(MovementPattern):
    def __init__(self, left_limit, right_limit, velocity, direction_interval, random_x=False):
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.velocity = velocity + 2
        self.random_x = random_x

        self.move_direction = 1
        self.change_interval = direction_interval
        self.since_change = 0

    def move(self, enemy):
        enemy.rect.x += self.velocity * self.move_direction
        # X boundary check
        if enemy.rect.right >= self.right_limit or enemy.rect.left <= self.left_limit:
            self.move_direction *= -1


        # direction change  
        if self.random_x:
            self.since_change += 1
            if self.since_change >= self.change_interval:
                if random.random() < 0.5:
                    self.move_direction *= -1
                self.since_change = 0    