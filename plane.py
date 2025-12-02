import pygame

class Plane(pygame.sprite.Sprite):
    def __init__(self, image_path, start_pos, end_pos, speed=2):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        
        self.pos = pygame.math.Vector2(start_pos)
        self.target = pygame.math.Vector2(end_pos)
        
        self.speed = speed
        
        direction = self.target - self.pos
        if direction.length() != 0:
            self.velocity = direction.normalize() * speed
        else:
            self.velocity = pygame.math.Vector2(0, 0)
    
    #will make the plane move it move it
    def update(self):
        if self.pos.distance_to(self.target) > self.speed:
            self.pos = self.pos + self.velocity
            self.rect.center = self.pos
        else:
            self.pos = self.target
            self.rect.center = self.target