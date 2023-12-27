import pygame, asyncio
from pygame.locals import *
from pygame.sprite import Group
from sprites import Player, Ghost

# Program constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BACKGROUND = (0, 0, 0)
FPS = 60

# Game initialization
pygame.init()
clock = pygame.time.Clock()

# Window initialization
pygame.display.set_caption('Ghosts')
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)

# Object making
player = Player(SCREEN_WIDTH/2, 300)
floor = pygame.Rect(0, 450, SCREEN_WIDTH, SCREEN_HEIGHT - 400)

# Game loop
async def main():
    running = True
    while running:
        # Dealing with events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        # Update
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys, floor)

        # Draw the frame
        screen.fill(BACKGROUND)
        pygame.draw.rect(screen, (100,100,128), pygame.Rect(75, 100, SCREEN_WIDTH - 150, SCREEN_HEIGHT-75))
        pygame.draw.rect(screen, (128,128,128), floor)
        player.draw(screen)


        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)
asyncio.run(main())