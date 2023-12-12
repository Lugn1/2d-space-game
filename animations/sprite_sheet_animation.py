import pygame

class SpriteSheetAnimation:
    def __init__(self, img, rows, cols, position, frame_rate=60):
        self.img = img
        self.rows = rows
        self.cols = cols
        self.position = position
