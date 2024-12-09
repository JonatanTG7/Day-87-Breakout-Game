import pygame

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (255, 0, 0)  
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self,paddle):
        self.x += self.speed_x
        self.y += self.speed_y

        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

        if self.x - self.radius < 0 or self.x + self.radius > self.screen_width:
            self.speed_x *= -1

        if self.y - self.radius < 0:
            self.speed_y *= -1

        if self.y + self.radius > paddle.y and self.y + self.radius < paddle.y + paddle.height:
            if self.x > paddle.x and self.x < paddle.x + paddle.width:
                self.speed_y *= -1  
        
        if self.y + self.radius > self.screen_height:
            print("Game Over!")
            self.reset()

    def check_collision_with_bricks(self, bricks):
        for brick in bricks:
            if brick.alive and self.rect.colliderect(brick.rect):   
                brick.alive = False 
                self.speed_y *= -1  
                return 1
                

    def reset(self):
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        self.speed_x *= -1  
        self.speed_y = -abs(self.speed_y)  