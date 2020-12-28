from StarryNight import StarryNight

from win32api import GetSystemMetrics
import sys
import pygame

# ________________ PYGAME SETUP ________________ #
fullscreen = False
if fullscreen:
    systemWidth = GetSystemMetrics(0)
    systemHeight = GetSystemMetrics(1)
    screen = pygame.display.set_mode((systemWidth, systemHeight), pygame.FULLSCREEN)
else:
    systemWidth = 500
    systemHeight = 500
    screen = pygame.display.set_mode((systemWidth, systemHeight))
pygame.display.set_caption("Minimal Pygame Window")

clock = pygame.time.Clock()
FPS = 30

# ________________ GAME LOOP ________________ #
nightly = StarryNight(systemWidth, systemHeight, 25, screen)
nightly.create_nodes()

col_background = (31, 71, 87)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.get_surface().fill(col_background)  # background
    nightly.render()  # render the starry night

    pygame.display.flip()  # update screen
    clock.tick(FPS)
