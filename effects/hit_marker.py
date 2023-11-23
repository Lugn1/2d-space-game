import pygame

class HitMarker: 
    def __init__(self, x, y, duration=3):
        self.x = x
        self.y = y
        self.duration = duration
        self.current_duration = 0


    def draw(self, win):
        if self.current_duration < self.duration:
            marker_color = (255, 0, 0)
            marker_length = 10
            pygame.draw.line(win, marker_color, (self.x, self.y), (self.x + marker_length, self.y), 2)  # Top line
            pygame.draw.line(win, marker_color, (self.x, self.y), (self.x, self.y + marker_length), 2)  # Left line
            pygame.draw.line(win, marker_color, (self.x + marker_length, self.y), (self.x, self.y), 2)  # Bottom line
            pygame.draw.line(win, marker_color, (self.x, self.y + marker_length), (self.x, self.y), 2)  # Right line
            self.current_duration += 1