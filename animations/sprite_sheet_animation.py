import pygame

class SpriteSheetAnimation:
    def __init__(self, img, rows, cols, position, frame_rate=60, loop=True, scale=1, health_based=False):
        self.rows = rows
        self.cols = cols
        self.position = position
        self.frame_rate = frame_rate
        self.loop = loop
        self.scale = scale
        
        if self.scale != 1:
            img_width, img_height = img.get_size()
            img = pygame.transform.scale(img, (int(img_width * self.scale), int(img_height * self.scale)))

        self.img = img
        self.total_frames = self.rows * self.cols
        self.frame_width = self.img.get_width() // self.cols
        self.frame_height = self.img.get_height() // self.rows
        self.frames = self.create_frames()
        self.current_frame = 0 
        self.start_time = pygame.time.get_ticks()
        self.completed = False
        self.health_based = health_based

        if self.health_based:
            self.health_frame_ranges = {
                "high": range(0, 10),
                "medium": range(10, 20),
                "low": range(20, 30),
                "critical": range(30, 40)
            }
            self.current_frame_range = self.health_frame_ranges["high"]
        else:
            self.current_frame_range = range(0, self.total_frames)    

    def create_frames(self):
        frames = []
        for row in range(self.rows):
            for col in range(self.cols):
                frame_rect = (col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)
                frames.append(self.img.subsurface(frame_rect))
        return frames  


    def update(self, health_percentage=None):
        if self.health_based and health_percentage is not None:
            if self.health_based and health_percentage is not None:
            # Determine the frame range based on the entity's health
                if health_percentage > 75:
                    self.current_frame_range = self.health_frame_ranges["high"]
                elif health_percentage > 50:
                    self.current_frame_range = self.health_frame_ranges["medium"]
                elif health_percentage > 25:
                    self.current_frame_range = self.health_frame_ranges["low"]
                else:
                    self.current_frame_range = self.health_frame_ranges["critical"]

            # Update the current frame within the selected range
            self.current_frame = (self.current_frame + 1) % len(self.current_frame_range)
            self.current_frame_index = self.current_frame_range[self.current_frame]
        else:
            # Regular animation logic (if not health-based)
            self.current_frame = (self.current_frame + 1) % self.total_frames
            self.current_frame_index = self.current_frame
        if not self.completed:
        # Update the time and change the frame.
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.frame_rate:
                self.current_frame += 1
                self.start_time = current_time
                if self.current_frame >= self.total_frames:
                    if self.loop:
                        self.current_frame = 0
                    else:
                        self.current_frame = self.total_frames - 1  # Stay on the last frame
                        self.completed = True
        

    def draw(self, surface):
        if not self.completed:
            top_left_pos = (self.position[0] - self.frame_width // 2, self.position[1] - self.frame_height // 2)
            frame = self.frames[self.current_frame]
            surface.blit(frame, top_left_pos)

    
