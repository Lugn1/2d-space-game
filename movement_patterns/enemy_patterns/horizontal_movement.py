from movement_patterns.movement_pattern import MovementPattern

class EnemyHorizontalMovementPattern(MovementPattern):
    def __init__(self, left_limit, right_limit, velocity):
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.velocity = velocity

        self.move_direction = 1

    def move(self, enemy):
        enemy.rect.x += self.velocity * self.move_direction
        # X boundary check
        if enemy.rect.right >= self.right_limit or enemy.rect.left <= self.left_limit:
            self.move_direction *= -1

    