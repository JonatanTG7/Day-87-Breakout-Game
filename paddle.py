import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed, screen_width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.screen_width = screen_width

    def draw(self, screen):
        pygame.draw.rect(screen, (64, 64, 64), (self.x, self.y, self.width, self.height))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        if self.x < 0:
            self.x = 0
        if self.x + self.width > self.screen_width:
            self.x = self.screen_width - self.width



