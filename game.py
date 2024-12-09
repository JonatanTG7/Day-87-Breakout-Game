from random import randint
import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick


pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

running  = True
current_screen = "menu"
clicked = False
ball_moving = False
game_over = False

pygame.display.set_caption('Breakout Game')

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Define the font
font_button = pygame.font.SysFont(None, 30)
font_text_title = pygame.font.SysFont("Arial" , 60 , bold=True)

#Background of FC Bayern Munchen
img_num =randint(1,4)
background_img = pygame.image.load(f"images/img{img_num}.jpg").convert()
scaled_image = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_text(text,font,text_color,x,y,center=False, bg_color_label=None):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y) 
    pygame.draw.rect(screen, bg_color_label, text_rect)
    screen.blit(text_surface, text_rect)

class button():

    #Colors for button types 
    button_color = (192,192,192)
    hover_color = (255,51,51)
    click_color = (153,0,0)
    text_color = (0,0,0)
    width = 180
    height = 40

    def __init__(self,x,y,text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):
        global clicked
        action = False

        #Get mouse position
        pos = pygame.mouse.get_pos()

        #Pygame Rect object for the button
        button_rect = pygame.Rect(self.x , self.y , self.width , self.height)

        #check mousrover and click conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_color , button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen , self.hover_color , button_rect)
        else:
            pygame.draw.rect(screen , self.button_color , button_rect)

        text_img = font_button.render(self.text , True , self.text_color)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width/2) - int(text_len/2), self.y+5))
        return action


start = button(400,500, "Start")
ranking = button(400,600, "Ranking")
game_info = button(400,700, "Info")

paddle = Paddle(x=400, y=900, width=200, height=25, speed=10, screen_width=SCREEN_WIDTH)
ball = Ball(x=500, y=500, radius=10, speed_x=5, speed_y=5, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

brick_width = 95
brick_height = 20
horizontal_gap = 20
vertical_gap = 20
start_y = 75 
bricks = []

for row in range(6): 
    for col in range(8): 
        brick_x = col * (brick_width + horizontal_gap) + 50
        brick_y = row * (brick_height + vertical_gap) + start_y
        brick = Brick(brick_x, brick_y, brick_width, brick_height)
        bricks.append(brick)

remaining_bricks = len(bricks)
def draw_counters():
    draw_text(f"Remaining: {remaining_bricks}", font_button, (0,0,0),  100 , 25, center=True,bg_color_label=(255,255,255)) 

remaining_lives = 3 
def draw_lives():
    draw_text(f"Lives: {remaining_lives}",font_button, (0,0,0),  800 , 25, center=True,bg_color_label=(255,255,255))

def handle_life_loss(): 
    print(f"Lives left: {remaining_lives}")
    if remaining_lives <= 0:
        print("Game Over!")
        return False  
    return True  


def draw_game_over(screen):
    draw_text(f"Game Over! Destroyed Bricks: {48 - remaining_bricks}", font_button ,(0,0,0),  SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2, center=True,bg_color_label=(192,192,192))


def reset_game():
    global remaining_bricks, remaining_lives, bricks, ball, paddle,game_over
    remaining_lives = 3
    game_over = False
    bricks = []
    for row in range(6): 
        for col in range(8): 
            brick_x = col * (brick_width + horizontal_gap) + 50
            brick_y = row * (brick_height + vertical_gap) + start_y
            brick = Brick(brick_x, brick_y, brick_width, brick_height)
            bricks.append(brick)
    remaining_bricks = len(bricks)
    ball.reset()  
    paddle.x = SCREEN_WIDTH // 2 - paddle.width // 2  

while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running  = False

    if current_screen == "menu":
        screen.blit(scaled_image,(0,0))
        draw_text("Welcome to FC Bayern", font_text_title ,(0,0,0),  SCREEN_WIDTH // 2, 100, center=True,bg_color_label=(192,192,192))
        draw_text("Breakout Game", font_text_title ,(0,0,0), SCREEN_WIDTH // 2, 300, center=True,bg_color_label=(192,192,192))

        if start.draw_button():
            print("Start")
            current_screen = "game"
        if ranking.draw_button():
            print("Ranking")
        if game_info.draw_button():
            print("game_info")

    elif current_screen == "game":
        screen.blit(scaled_image, (0, 0))

        paddle.update()
        paddle.draw(screen)

        for brick in bricks:
            brick.draw(screen)

        ball.draw(screen)
        if paddle.x > 400 or paddle.x < 400:
            ball_moving = True
        if not game_over:
            if ball_moving:
                ball.update(paddle)
                ball.draw(screen)
        
        if ball.check_collision_with_bricks(bricks):
            remaining_bricks -=1

        draw_counters()
        draw_lives()
        if ball.losing_life():
            remaining_lives -=1
            if not handle_life_loss():
                game_over = True

        if game_over: 
            draw_game_over(screen)
            Restart = button(400,550, "Restart")
            if Restart.draw_button():
                current_screen = "menu" 
                reset_game()  
                 

        

    pygame.display.flip()

    clock.tick(60)

pygame.quit()