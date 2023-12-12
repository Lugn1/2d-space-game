import pygame

class SpriteSheetAnimation:
    def __init__(self, img, rows, cols, position, frame_rate=60, loop=True):
        self.img = img
        self.rows = rows
        self.cols = cols
        self.position = position
        self.frame_rate = frame_rate
        self.loop = loop

        self.total_frames = self.rows * self.cols
        self.frame_width = self.img.get_width() // self.cols
        self.frame_height = self.img.get_height() // self.rows
        self.frames = self.create_frames()
        self.current_frame = 0 
        self.start_time = pygame.time.get_ticks()
        self.completed = False

    def create_frames(self):
        frames = []
        for row in range(self.rows):
            for col in range(self.cols):
                frame_rect = (col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)
                frames.append(self.img.subsurface(frame_rect))
        return frames  


    def update(self):
        if not self.completed:
            if pygame.time.get_ticks() - self.start_time >= self.frame_rate:
                self.current_frame += 1
                self.start_time = pygame.time.get_ticks()
                if self.current_frame >= self.total_frames:
                    if self.loop:
                        self.current_frame = 0
                    else:
                        self.current_frame -= 1
                        self.completed = True         

    def draw(self, surface):
        if not self.completed:
            frame = self.frames[self.current_frame]
            surface.blit(frame, self.position)