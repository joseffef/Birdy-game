import pygame
import random
import sys
import tkinter
from tkinter import PhotoImage

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 45
GRAVITY = 1        
JUMP = -15
PIPE_WIDTH = 300
PIPE_GAP = 350


# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load images (using simple rectangles for this example)
bird_img = pygame.image.load(r"C:\Users\dahri\Downloads\ghlioda-removebg-preview.png")
bird_img = pygame.transform.scale(bird_img,  (bird_img.get_width() //2 , bird_img.get_height() //2))
pipe_img = pygame.image.load(r"C:\Users\dahri\Downloads\pipe-removebg-preview.png").convert_alpha()

# Load the background image
background_img = pygame.image.load(r"C:\Users\dahri\Downloads\fond ecran.jpg").convert_alpha()
background_img = pygame.transform.scale(background_img, (400, 600))

class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel = 0
        self.image = pygame.image.load(r"C:\Users\dahri\Downloads\ghlioda-removebg-preview.png")
        self.image = pygame.transform.scale(self.image,  (self.image.get_width() //2, self.image.get_height() //2))
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)
        
    def jump(self):
        self.vel = JUMP

    def draw(self, win):
        win.blit(bird_img, (self.x, self.y))
       

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)
    
    def update(self):
        self.x -= 5
        self.top.topleft = (self.x, 0)
        self.bottom.topleft = (self.x, self.height + PIPE_GAP)

    def draw(self, win):
        
        pygame.draw.rect(win, "black", self.top)
        pygame.draw.rect(win, "black", self.bottom)

def game_over(win, score): 
    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
                    
    game_over_text = font_big.render("Game Over", True, "red")
    score_text = font_big.render(f"Score: {score}", True, "red")
    restart_text = font_small.render("Press R to Restart or Q to Quit", True, "red")

    win.fill("black")
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    win.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.update()

    wait_for_exit()

def wait_for_exit():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    return
                
def start_screen(win):
    font_title = pygame.font.SysFont(None, 72)
    font_instructions = pygame.font.SysFont(None, 36)

    # Load background image or create a gradient
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill("red")

    title_text = font_title.render("Flappy Bird", True, "black")
    instructions_text = font_instructions.render("Press SPACE to Start", True, "black")
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return    # Start the game
                    
        win.blit(background, (0, 0))
        win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        win.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2))

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    font = pygame.font.SysFont(None, 36)
    last_pipe_passed = 0

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_q:
                    run = False
            # Update bird
        bird.update()

            # Update pipes
        if pipes[-1].x < WIDTH // 2:
            pipes.append(Pipe())

            # Remove off-screen pipes and update score
        for pipe in pipes[:]:
            pipe.update()
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                score += 1

            # Check for collisions
        for pipe in pipes:
            if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                game_over(win, score)
                run = False
                    
                 # Increment score if bird has passed the pipe
            if pipe.x + PIPE_WIDTH < bird.x and last_pipe_passed < pipe.x:
                    score += 1
                    last_pipe_passed = pipe.x  # Update last passed pipe

            # Check for out-of-bounds (falling off the screen)
            if bird.y > HEIGHT or bird.y < 0:
                game_over(win, score)
                run = False  # End the game loop if the bird goes out of bounds

            # Drawing everything
            win.blit(background_img, (0, 0))  # Clear the screen
            bird.draw(win)  # Draw the bird
            for pipe in pipes:
                pipe.draw(win)  # Draw the pipes 

            # Draw the score
            score_text = font.render(f"Score: {score}", True, "pink")
            win.blit(score_text, (10, 10)) 
            pygame.display.update()  # Update the display

if __name__ == "__main__":
    start_screen(win) 
    main()