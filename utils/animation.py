import pygame
# TODO fix this 
# TODO fix import
# Todo fix folder name
class Animation:
    def __init__(self, img, row, col, x, y, width, height):
        self.frames = [img.subsurface((i * width, j * height, width, height))
                       for j in range(row) for i in range(col)]
        self.current_frame = 0
        self.x = x - width // 2 
        self.y = y - height // 2 
        self.done = False

    def update(self):
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.done = True

    def draw(self, win):
        if not self.done:
            win.blit(self.frames[self.current_frame], (self.x, self.y))
            self.update()