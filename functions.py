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


def main_menu(screen, screen_size: tuple, joke_text: str):
    """
    *************** Drawing Main Menu ***************
    """
    title = "Fisiks"
    title_font_size = int(screen_size[1] * 0.12)

    buttons_font_size = int(screen_size[1] * 0.06)
    button_width = int(screen_size[0] * 0.15)
    button_height = int(screen_size[1] * 0.08)

    title_y = screen_size[1] * 0.1
    button_x = screen_size[0] * 0.05
    play_button_y = screen_size[1] * 0.38
    settings_button_y = screen_size[1] * 0.5
    quit_button_y = screen_size[1] * 0.62

    title_font = pygame.font.SysFont("Calibri", title_font_size, bold=True)
    text_surface = title_font.render(title, True, [0, 0, 0])
    buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)
    
    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, title_y))
    screen.blit(text_surface, text_rect) # Title

    box_font_size = int(screen_size[1] * 0.04)
    text_box_width = int(screen_size[0] * 0.10)
    text_box_height = int(screen_size[1] * 0.2)

    text_box_x = screen_size[0] * 0.8
    text_box_y = screen_size[1] * 0.5

    clean_text = ""
    box_font = pygame.font.SysFont("Calibri", box_font_size)
    question_count = 0
    for i in joke_text:
        if i == "?":
            question_count += 1
        if i == "%":
            box_surface = box_font.render(clean_text, True, [0, 0, 0])
            box_rect = box_surface.get_rect(size = (text_box_width, text_box_height), center = (text_box_x, text_box_y))
            screen.blit(box_surface, box_rect) # Right text in box
            text_box_y += screen_size[1]*0.05
            clean_text = ""
        if question_count == 2 and i == "?":
            text_box_y += screen_size[1]*0.05
            clean_text = ""
        else:
            if not i == "%":
                clean_text += i
    box_surface = box_font.render(clean_text, True, [0, 0, 0])
    box_rect = box_surface.get_rect(size = (text_box_width, text_box_height), center = (text_box_x, text_box_y))
    screen.blit(box_surface, box_rect) # Right text in box

    box_width = screen_size[0] * 0.28
    box_height = screen_size[1] * 0.5
    box_x = screen_size[0] * 0.7
    box_y = screen_size[1] * 0.275

    pygame.draw.rect(screen, [0, 0, 0], [box_x, box_y, box_width, box_height], 2) # Draw box on the right

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


def select_joke(screen_size: tuple):
    n = random.randint(0, 49)
    with open(".\\assets\\jokes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    raw_text = data[n]['joke']
    raw_text = raw_text.split(' ')
    count = 0
    text = ""
    aspect_ratio = screen_size[0] // screen_size[1]
    for i in raw_text:
        if count == aspect_ratio*4:
            text += "%"
            count = 0
        text += i + " "
        count += 1
    return text


def play_menu(screen):
    screen.fill("blue")


def settings_menu(screen):
    screen.fill("red")


