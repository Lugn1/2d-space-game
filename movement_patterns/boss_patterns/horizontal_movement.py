import random
from movement_patterns.movement_pattern import MovementPattern


class HorizontalMovementPattern(MovementPattern):
    def __init__(self, left_limit, right_limit, velocity, direction_interval):
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.velocity = velocity
        self.move_direction = 1
        self.change_interval = direction_interval
        self.since_change = 0


    def move(self, boss):
        boss.rect.x += self.velocity * self.move_direction
        # X boundary check
        if boss.rect.right >= self.right_limit or boss.rect.left <= self.left_limit:
            self.move_direction *= -1

        # direction change  
        self.since_change += 1
        if self.since_change >= self.change_interval:
            if random.random() < 0.5:
                self.move_direction *= -1
            self.since_change = 0    