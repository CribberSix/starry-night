import sys
import pygame
from src.StarryNight import StarryNight

# ________________ PYGAME SETUP ________________ #
systemWidth = 900
systemHeight = 600
screen = pygame.display.set_mode((systemWidth, systemHeight))
pygame.display.set_caption("Starry night")
clock = pygame.time.Clock()
FPS = 30

# ________________ GAME LOOP ________________ #
nightly = StarryNight(25)
col_background = (13, 14, 23)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.get_surface().fill(col_background)  # background
    nightly.render()  # render the starry night

    pygame.display.flip()  # update screen
    clock.tick(FPS)
