from movement_patterns.movement_pattern import MovementPattern

class FollowingPlayerPattern(MovementPattern):
    def __init__(self, player, velocity):
        self.player = player
        self.velocity = velocity

    def move(self, boss):
        if boss.rect.x < self.player.rect.x:
            boss.rect.x += self.velocity
        elif boss.rect.x > self.player.rect.x:
            boss.rect.x -= self.velocity