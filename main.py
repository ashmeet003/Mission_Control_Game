# Ashmeet Kaur
# CompB10 Fall 2025
# Pygame
# Spirits are drawn using 3D paint in Windows
# Game is similar to flapping bird or endless runner
# User is free to move up/down/left/right

import pygame
import random
from pygame.locals import *

# -------------------------
# Player
# -------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):     # loads player sprite, makes its white background transparent
        super().__init__()
        self.surf = pygame.image.load("images/rocket.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(120, SCREEN_HEIGHT // 2))

    def update(self, keys):   # keys to move player
        # Normal movement
        if keys[K_UP]:
            self.rect.y -= 5
        if keys[K_DOWN]:
            self.rect.y += 5
        if keys[K_LEFT]:
            self.rect.x -= 5
        if keys[K_RIGHT]:
            self.rect.x += 5

        # Keep on-screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.left = 0



# -------------------------
# Pipe
# -------------------------
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()

        # Load pipe image
        self.surf = pygame.image.load("images/mountain.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # The following code is meant for pipes/ enemy sprite to appear mostly on upside or bottom
        # Random height like Flappy Bird
        top_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        # Top pipe rectangle
        self.top_rect = self.surf.get_rect(midbottom=(x, top_height))
        # Bottom pipe rectangle
        self.bottom_rect = self.surf.get_rect(midtop=(x, top_height + PIPE_GAP))

    def update(self):
        global score
        self.top_rect.x -= SCROLL_SPEED         # for pipe moving right to left
        self.bottom_rect.x -= SCROLL_SPEED
        # When pipe moves out of screen, score +1
        if self.top_rect.right < 0:
            score += 1
            self.kill()

    def draw(self, surface):                # to blit the pipes
        surface.blit(self.surf, self.top_rect)
        surface.blit(self.surf, self.bottom_rect)


# -------------------------
# Game Setup
# -------------------------

pygame.init()

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCROLL_SPEED = 4
PIPE_SPACING = 280          # distance between pipes (horizontal spacing)
PIPE_GAP = 170              # vertical gap for the player to pass through
score = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mission Control")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
background = pygame.image.load("images/spaceBackground.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sprites loading
player = Player()
all_pipes = pygame.sprite.Group()

# Pre-generate pipes in a row
for i in range(4):
    pipe_x = SCREEN_WIDTH + i * PIPE_SPACING
    pipe = Pipe(pipe_x)
    all_pipes.add(pipe)

running = True


# -------------------------
# MAIN LOOP
# -------------------------
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed() # when up/down/left/right is pressed
    player.update(keys)

    # Scroll pipes
    all_pipes.update()

    # If last pipe moves far enough, add a new one
    if len(all_pipes) < 4:
        new_x = max(pipe.top_rect.x for pipe in all_pipes) + PIPE_SPACING
        all_pipes.add(Pipe(new_x))

    # Collision
    for pipe in all_pipes:
        if player.rect.colliderect(pipe.top_rect) or player.rect.colliderect(pipe.bottom_rect):
            # --- SHOW END GAME MESSAGE ---
            end_font = pygame.font.Font(None, 72)
            end_text = end_font.render(f"GAME OVER   Score: {score}", True, (255, 255, 255))
            screen.blit(end_text, (
                SCREEN_WIDTH // 2 - end_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - end_text.get_height() // 2
            ))
            pygame.display.flip()
            pygame.time.delay(2500)
            running = False

    # --- DRAW / Loads space background image ---
    screen.blit(background, (0, 0))

    # draws all pipes/enemy sprites
    for pipe in all_pipes:
        pipe.draw(screen)

    screen.blit(player.surf, player.rect)

    # Score
    surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(surface, (10, 10))

    pygame.display.flip()   #flips screen
    clock.tick(35)          # game is set for speed 35

pygame.quit()
