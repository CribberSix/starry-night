import pygame
import sys
from src.StarryNight import StarryNight

screen = pygame.display.set_mode((900, 600))
nightly = StarryNight(25)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.get_surface().fill((31, 71, 87))  # background
    nightly.render()  # render the starry night
    pygame.display.flip()  # update screen
    pygame.time.Clock().tick(30)
