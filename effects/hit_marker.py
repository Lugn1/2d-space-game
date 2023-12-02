import pygame

class HitMarker: 
    def __init__(self, x, y, obj_width, obj_height, duration=3):
        self.center_x = x + obj_width / 2
        self.center_y = y + obj_height / 2
        self.duration = duration
        self.current_duration = 0
        # Define the corners of the bounding box
        self.c1 = (x, y)
        self.c2 = (x + obj_width, y)
        self.c3 = (x + obj_width, y + obj_height)
        self.c4 = (x, y + obj_height)
        
        


    def draw(self, win):
        if self.current_duration < self.duration:
            marker_color = (255, 0, 0) 
            marker_length = 20 
            line_thickness = 3   

            # Draw lines starting from each corner towards the center
            # Top-left corner (C1)
                            #Surface,ColorValue,  start_pos,        end_pos,                            width
            pygame.draw.line(win, marker_color, self.c1, (self.c1[0] + marker_length, self.c1[1]), line_thickness)
            pygame.draw.line(win, marker_color, self.c1, (self.c1[0], self.c1[1] + marker_length), line_thickness)
            
            # Top-right corner (C2)
            pygame.draw.line(win, marker_color, self.c2, (self.c2[0] - marker_length, self.c2[1]), line_thickness)
            pygame.draw.line(win, marker_color, self.c2, (self.c2[0], self.c2[1] + marker_length), line_thickness)
            
            # Bottom-right corner (C3)
            pygame.draw.line(win, marker_color, self.c3, (self.c3[0] - marker_length, self.c3[1]), line_thickness)
            pygame.draw.line(win, marker_color, self.c3, (self.c3[0], self.c3[1] - marker_length), line_thickness)
            
            # Bottom-left corner (C4)
            pygame.draw.line(win, marker_color, self.c4, (self.c4[0] + marker_length, self.c4[1]), line_thickness)
            pygame.draw.line(win, marker_color, self.c4, (self.c4[0], self.c4[1] - marker_length), line_thickness)
        self.current_duration += 1