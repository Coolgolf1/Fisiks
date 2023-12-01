import pygame
import numpy as np
import pymunk

def screen():
    global screen, screen_width, screen_height, window_size
    screen_width = 800
    screen_height = 600
    window_size = (screen_width,screen_height)
    screen = pygame.display.set_mode(window_size)

def menu_screen():
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Game Over', True, (0, 0, 0))
    restart_button = font.render('R - Restart', True, (0, 0, 0))
    quit_button = font.render('Q - Quit', True, (0, 0, 0))
    screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height()/3))
    screen.blit(restart_button, (screen_width/2 - restart_button.get_width()/2, screen_height/1.9 + restart_button.get_height()))
    screen.blit(quit_button, (screen_width/2 - quit_button.get_width()/2, screen_height/2 + quit_button.get_height()/2))

