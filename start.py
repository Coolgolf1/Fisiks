import pygame
import numpy as np
import pymunk

pygame.init()

window_size = (800,600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Pygame Window")

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic goes here

    # Drawing on the screen
    window.fill((255, 255, 255))  # Fill the window with black color

    # Update the display
    pygame.display.flip()

pygame.quit()
