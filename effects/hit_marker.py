import pygame

class HitMarker: 
    def __init__(self, x, y, duration=3):
        self.x = x
        self.y = y
        self.duration = duration
        self.current_duration = 0


    def draw(self, win):
        if self.current_duration < self.duration:
            marker_color = (255, 0, 0)  # Red color
            marker_length = 20  # Length of each line segment
            line_thickness = 2  # Thickness of the lines
            gap = 10  # Gap between the center of the ship and the start of the lines

            # Calculate the end points for each line, with a gap from the center
            # Top line
            pygame.draw.line(win, marker_color, (self.x, self.y - gap), (self.x, self.y - marker_length - gap), line_thickness)
            # Bottom line
            pygame.draw.line(win, marker_color, (self.x, self.y + gap), (self.x, self.y + marker_length + gap), line_thickness)
            # Left line
            pygame.draw.line(win, marker_color, (self.x - gap, self.y), (self.x - marker_length - gap, self.y), line_thickness)
            # Right line
            pygame.draw.line(win, marker_color, (self.x + gap, self.y), (self.x + marker_length + gap, self.y), line_thickness)

            # Increment the duration
        self.current_duration += 1