import pygame
import random

pygame.init()
infoObject = pygame.display.Info()

# Screen dimensions
W = infoObject.current_w - 100  
H = infoObject.current_h - 100  

# Colours
white = (128, 128, 128)
black = (0, 0, 0)
red = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((W, H))
bg = pygame.image.load("background.jpeg")
bg = pygame.transform.scale(bg, (W, H))

# Bar dimensions and position
w, h = 170, 30
bar_x, bar_y = W / 2 - w / 2, H - 150
move_x, move_y = 0, 0

# Ball properties
ball_radius = 10
ball_x, ball_y = W // 2, H - 200
# Ball speed
ball_speed_x, ball_speed_y = 0.5, -0.5  

# Brick properties
brick_rows = 5
brick_cols = 10
brick_width = W // brick_cols
brick_height = 30
bricks = [[True for _ in range(brick_cols)] for _ in range(brick_rows)]

# Set to track pressed keys
keys_pressed = set()

# Function to display Starting Menu
def starting_menu():
    font = pygame.font.SysFont(None, 60)
    title_text = font.render("THE BRICK BREAKER", True, red)
    start_text = font.render("Press ENTER to Start", True, white)
    quit_text = font.render("Press ESCAPE to Quit", True, white)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game
                    return
                if event.key == pygame.K_ESCAPE:  # Quit game
                    pygame.quit()
                    quit()

        screen.blit(bg, (0, 0))
        screen.blit(title_text, (W // 2 - title_text.get_width() // 2, H // 2 - title_text.get_height() // 2 - 50))
        screen.blit(start_text, (W // 2 - start_text.get_width() // 2, H // 2 + 20))
        screen.blit(quit_text, (W // 2 - quit_text.get_width() // 2, H // 2 + 80))
        pygame.display.update()

# Function to display Game Over screen
def game_over():
    font = pygame.font.SysFont(None, 60)
    text = font.render("GAME OVER!", True, red)  
    restart_text = font.render("Press Space to Restart.", True, white) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    start_game() 
        
        screen.blit(bg, (0, 0)) 
        screen.blit(text, (W // 2 - text.get_width() // 2, H // 2 - text.get_height() // 2 - 50))  
        screen.blit(restart_text, (W // 2 - restart_text.get_width() // 2, H // 2 + 50))  
        pygame.display.update()

# Function to display the Pause Menu
def show_menu():
    font = pygame.font.SysFont(None, 60)
    title_text = font.render("GAME PAUSED", True, red)
    resume_text = font.render("Press ENTER to Resume", True, white)
    quit_text = font.render("Press ESCAPE to Quit", True, white)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Resume game
                    return
                if event.key == pygame.K_ESCAPE:  # Quit game
                    pygame.quit()
                    quit()

        screen.blit(bg, (0, 0))
        screen.blit(title_text, (W // 2 - title_text.get_width() // 2, H // 2 - title_text.get_height() // 2 - 50))
        screen.blit(resume_text, (W // 2 - resume_text.get_width() // 2, H // 2 + 20))
        screen.blit(quit_text, (W // 2 - quit_text.get_width() // 2, H // 2 + 80))
        pygame.display.update()

# Function to start/restart the game
def start_game():
    global bar_x, bar_y, ball_x, ball_y, ball_speed_x, ball_speed_y, bricks
    # Reset paddle, ball, and brick positions
    bar_x, bar_y = W / 2 - w / 2, H - 150
    ball_x, ball_y = W // 2, H - 200
    ball_speed_x, ball_speed_y = 0.5, -0.5
    bricks = [[True for _ in range(brick_cols)] for _ in range(brick_rows)]
    game_loop()

# Main game loop
def game_loop():
    global bar_x, bar_y, ball_x, ball_y, ball_speed_x, ball_speed_y, keys_pressed, bricks

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                keys_pressed.add(event.key)
                if event.key == pygame.K_ESCAPE:  # Trigger menu
                    show_menu()
            if event.type == pygame.KEYUP:
                keys_pressed.discard(event.key)

        # Reset movement
        move_x, move_y = 0, 0

        # Determine movement based on keys pressed
        if pygame.K_LEFT in keys_pressed and pygame.K_RIGHT not in keys_pressed:
            move_x = -1
        if pygame.K_RIGHT in keys_pressed and pygame.K_LEFT not in keys_pressed:
            move_x = 1

        # Update bar position
        bar_x += move_x
        bar_y += move_y

        # Bar position constraints
        bar_x = max(0, min(W - w, bar_x))
        bar_y = max(0, min(H - h, bar_y))

        # Update ball position
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with walls
        if ball_x - ball_radius < 0 or ball_x + ball_radius > W:
            ball_speed_x *= -1
        if ball_y - ball_radius < 0:
            ball_speed_y *= -1

        # Ball collision with paddle
        if (bar_x < ball_x < bar_x + w) and (bar_y < ball_y + ball_radius < bar_y + h):
            ball_speed_y *= -1

        # Ball collision with bricks
        for row in range(brick_rows):
            for col in range(brick_cols):
                if bricks[row][col]:
                    brick_x = col * brick_width
                    brick_y = row * brick_height
                    if (brick_x < ball_x < brick_x + brick_width) and (brick_y < ball_y < brick_y + brick_height):
                        bricks[row][col] = False
                        ball_speed_y *= -1
                        break

        # Game over condition
        if ball_y > H:
            game_over()

        # Drawing elements
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, white, [bar_x, bar_y, w, h])  # Paddle
        pygame.draw.circle(screen, red, (ball_x, ball_y), ball_radius)  # Ball
        for row in range(brick_rows):  # Bricks
            for col in range(brick_cols):
                if bricks[row][col]:
                    brick_x = col * brick_width
                    brick_y = row * brick_height
                    pygame.draw.rect(screen, white, [brick_x, brick_y, brick_width, brick_height])

        pygame.display.update()

# Display starting menu
starting_menu()
# Start the game
start_game()