import pygame

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.alive = True  

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, YELLOW, self.rect)  
            pygame.draw.rect(screen, BLACK, self.rect, 5) 