import pygame
import numpy as np
import pymunk
from classes import *
import random
import json


def print_screen(screen, screen_size: tuple):
    pygame.display.set_caption("Fisiks")
    bg = pygame.image.load(".\\assets\\background.png")
    bg = pygame.transform.scale(bg, (screen_size[0], screen_size[1]))
    screen.blit(bg, (0, 0))


def main_menu(screen, screen_size: tuple):
    """
    *************** Drawing Main Menu ***************
    """
    title = "Fisiks"

    title_font_size = int(screen_size[1] * 0.12)

    # box_font_size = int(screen_size[1] * 0.02)

    buttons_font_size = int(screen_size[1] * 0.06)

    button_width = int(screen_size[0] * 0.15)
    button_height = int(screen_size[1] * 0.08)

    # box_width = int(screen_size[0] * 0.4)
    # box_height = int(screen_size[1] * 0.6)
    # box_x = screen_size[0] - box_width
    # box_y = (screen_size[1] - box_height) // 2

    title_y = screen_size[1] * 0.1
    button_x = screen_size[0] * 0.05
    play_button_y = screen_size[1] * 0.38
    settings_button_y = screen_size[1] * 0.5
    quit_button_y = screen_size[1] * 0.62

    # box_x = screen_size[0] * 0.95
    # box_y = screen_size[1] * 0.5

    title_font = pygame.font.SysFont("Calibri", title_font_size, bold=True)
    text_surface = title_font.render(title, True, [0, 0, 0])

    buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)

    # box_font = pygame.font.SysFont("Calibri", box_font_size)
    # box_text = wrapped_text(joke_text, box_font, box_width)
    # current_y = box_y
    # for line in wrapped_text:
    #     line_surface = box_font.render(line, True, [0, 0, 0])
    #     line_rect = line_surface.get_rect(topleft=(box_x, current_y))
    #     screen.blit(line_surface, line_rect)
    #     current_y += box_font.get_linesize()
    # button_surface = box_font.render(box_text, True, [0, 0, 0])

    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, title_y))

    # box_rect = button_surface.get_rect(size = (box_width, box_height), center = (box_x, box_y))

    screen.blit(text_surface, text_rect)

    # screen.blit(button_surface, box_rect)

    PlayButton = Button((button_x, play_button_y),
                        (button_width, button_height), 2, "Jugar")
    PlayButton.draw(screen, buttons_font)
    SettingsButton = Button((button_x, settings_button_y),
                            (button_width, button_height), 2, "Ajustes")
    SettingsButton.draw(screen, buttons_font)
    QuitButton = Button((button_x, quit_button_y),
                        (button_width, button_height), 2, "Salir")
    QuitButton.draw(screen, buttons_font)

    return PlayButton, SettingsButton, QuitButton


def select_joke():
    n = random.randint(0, 49)
    with open(".\\assets\\jokes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    text = data[n]['joke']
    return text


def play_menu(screen):
    screen.fill("blue")


def settings_menu(screen):
    screen.fill("red")
