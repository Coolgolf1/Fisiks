import pygame
import numpy as np
import pymunk
from classes import *
import random
import json
import pymunk.pygame_util


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
    screen.blit(text_surface, text_rect)  # Title

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
            box_rect = box_surface.get_rect(
                size=(text_box_width, text_box_height), center=(text_box_x, text_box_y))
            screen.blit(box_surface, box_rect)  # Right text in box
            text_box_y += screen_size[1]*0.05
            clean_text = ""
        if question_count == 2 and i == "?":
            text_box_y += screen_size[1]*0.05
            clean_text = ""
        else:
            if not i == "%":
                clean_text += i
    box_surface = box_font.render(clean_text, True, [0, 0, 0])
    box_rect = box_surface.get_rect(
        size=(text_box_width, text_box_height), center=(text_box_x, text_box_y))
    screen.blit(box_surface, box_rect)  # Right text in box

    box_width = screen_size[0] * 0.28
    box_height = screen_size[1] * 0.5
    box_x = screen_size[0] * 0.7
    box_y = screen_size[1] * 0.275

    # Draw box on the right
    pygame.draw.rect(screen, [0, 0, 0], [
                     box_x, box_y, box_width, box_height], 2)

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


def play_menu(screen, screen_size):
    screen.fill("white")
    button_x1 = screen_size[0] * 0.33
    button_x2 = screen_size[0] * 0.50
    button_x3 = screen_size[0] * 0.67
    buttons_font_size = int(screen_size[1] * 0.06)
    button_width = int(screen_size[0] * 0.15)
    button_height = int(screen_size[1] * 0.08)
    buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)

    Level1Button = Button((button_x1, 360),
                          (button_width, button_height), 2, "Nivel 1")
    Level1Button.draw(screen, buttons_font)
    Level2Button = Button((button_x2, 360),
                          (button_width, button_height), 2, "Nivel 2")
    Level2Button.draw(screen, buttons_font)
    Level3Button = Button((button_x3, 360),
                          (button_width, button_height), 2, "Nivel 3")
    Level3Button.draw(screen, buttons_font)

    return Level1Button, Level2Button, Level3Button


def buttons_in_game(screen_size):
    buttons_font_size_IG = int(screen_size[1] * 0.06)
    buttons_font_IG = pygame.font.SysFont(
        "Calibri", buttons_font_size_IG, True)
    # Restart Button
    RestartButtonIG = Button((screen_size[0]*0.06, screen_size[1]*0.005),
                             (screen_size[0]*0.05, screen_size[1]*0.05), 1, "R")
    RIGBPos = RestartButtonIG.position
    RIGBSize = RestartButtonIG.size
    # Menu Button
    MenuButtonIG = Button((screen_size[0]*0.005, screen_size[1]*0.005),
                          (screen_size[0]*0.05, screen_size[1]*0.05), 1, "M")
    MIGBPos = MenuButtonIG.position
    MIGBSize = MenuButtonIG.size
    return buttons_font_IG, RestartButtonIG, RIGBPos, RIGBSize, MenuButtonIG, MIGBPos, MIGBSize


def final_menu(screen_size):
    # End Box
    end = False
    text_box_width = int(screen_size[0] * 0.5)
    text_box_height = int(screen_size[1] * 0.5)
    text_box_x = (screen_size[0] - text_box_width) // 2
    text_box_y = (screen_size[1] - text_box_height) // 2
    # Box Enhorabuena
    box_font_size_congrats = int(screen_size[1] * 0.10)
    box_font_congrats = pygame.font.SysFont(
        "Calibri", box_font_size_congrats, True)
    center_x_congrats = screen_size[0] * 0.5
    center_y_congrats = screen_size[1] * 0.4
    box_surface_congrats = box_font_congrats.render(
        "¡Enhorabuena!", True, [0, 0, 0])
    box_rect_congrats = box_surface_congrats.get_rect(
        center=(center_x_congrats, center_y_congrats))
    # Count Text
    count = 0
    box_font_size_count_live = int(screen_size[1] * 0.08)
    box_font_count_live = pygame.font.SysFont(
        "Calibri", box_font_size_count_live, True)
    center_x_count_live = screen_size[0] * 0.5
    center_y_count_live = screen_size[1] * 0.05
    box_font_size_count = int(screen_size[1] * 0.06)
    box_font_count = pygame.font.SysFont("Calibri", box_font_size_count)
    center_x_count = screen_size[0] * 0.5
    center_y_count = screen_size[1] * 0.5
    # Buttons Font
    buttons_font_size = int(screen_size[1] * 0.06)
    buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)
    # Restart Button
    RestartButton = Button((screen_size[0]*0.27, screen_size[1]*0.58),
                           (screen_size[0]*0.15, screen_size[1]*0.1), 1, "Reiniciar")
    # Menu Button
    MenuButton = Button((screen_size[0]*0.45, screen_size[1]*0.58),
                        (screen_size[0]*0.1, screen_size[1]*0.1), 1, "Menú")
    # Next Level Button
    NextLevelButton = Button((screen_size[0]*0.58, screen_size[1]*0.58),
                             (screen_size[0]*0.15, screen_size[1]*0.1), 1, "Siguiente")
    return end, text_box_width, text_box_height, text_box_x, text_box_y, box_surface_congrats, box_rect_congrats, count, box_font_count_live, center_x_count_live, center_y_count_live, box_font_count, center_x_count, center_y_count, buttons_font, RestartButton, MenuButton, NextLevelButton


def level_1(screen, screen_size):
    clock = pygame.time.Clock()
    FPS = 144

    space = pymunk.Space()
    space.gravity = (0, 200)

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    space.debug_draw(draw_options)

    permanent_surface = pygame.Surface(screen.get_size())
    permanent_surface.fill("white")

    drawings = []
    points = []
    drawing = False
    lines = []
    jar_lines = []
    thickness = 10
    y_scalable_constant = 175/720
    menu_condition = False
    clicked = False
    quit_condition = False
    cancel = False

    # Black Lines
    lines.append(StaticLine(space, [(screen_size[0]*0.3125, screen_size[1] *
                 y_scalable_constant), (screen_size[0], screen_size[1]*y_scalable_constant)], 10))
    lines.append(StaticLine(space, [(0, screen_size[1]*y_scalable_constant*2),
                 (screen_size[0]*0.6875, screen_size[1]*y_scalable_constant*2)], 10))
    lines.append(StaticLine(space, [(screen_size[0]*0.15625, screen_size[1] *
                 y_scalable_constant*3), (screen_size[0], screen_size[1]*y_scalable_constant*3)], 10))
    # Triangles
    lines.append(StaticLine(space, [(0, (screen_size[1])*(100/720)*2),
                 (screen_size[0]*0.15625, screen_size[1]*y_scalable_constant*2)], 10))
    lines.append(StaticLine(space, [(screen_size[0], (screen_size[1])*(100/720)*4),
                 (screen_size[0]*0.84375, screen_size[1]*y_scalable_constant*3)], 10))
    # Limits
    lines.append(StaticLine(space, [(0, 0), (0, screen_size[1])], 1))
    lines.append(StaticLine(
        space, [(screen_size[0], 0), (screen_size[0], screen_size[1])], 1))
    lines.append(StaticLine(space, [(0, 0), (screen_size[0], 0)], 1))
    lines.append(StaticLine(
        space, [(0, screen_size[1]), (screen_size[0], screen_size[1])], 1))
    # Jar
    jar_lines.append(StaticLine(space, [
                     (screen_size[0]*0.0390625, screen_size[1]), (screen_size[0]*0.1171875, screen_size[1])], 5))
    jar_lines.append(StaticLine(space, [
                     (screen_size[0]*0.0390625, screen_size[1]), (0, screen_size[1]*y_scalable_constant*3)], 5))
    jar_lines.append(StaticLine(space, [(screen_size[0]*0.1171875, screen_size[1]),
                     (screen_size[0]*0.15625, screen_size[1]*y_scalable_constant*3)], 5))
    # Ball
    ball = Ball(space, (1200, 100), screen_size[1]*0.0555555555555556)
    # Testing Ball
    # ball = Ball(space, (100, 400), screen_size[1]*0.0555555555555556)

    end, text_box_width, text_box_height, text_box_x, text_box_y, box_surface_congrats, box_rect_congrats, count, box_font_count_live, center_x_count_live, center_y_count_live, box_font_count, center_x_count, center_y_count, buttons_font, RestartButton, MenuButton, NextLevelButton = final_menu(
        screen_size)

    buttons_font_IG, RestartButtonIG, RIGBPos, RIGBSize, MenuButtonIG, MIGBPos, MIGBSize = buttons_in_game(
        screen_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_condition = True
            if event.type == pygame.MOUSEBUTTONDOWN and not end:
                if not cancel:
                    points = [event.pos]
                    drawing = True
                cancel = False
            if event.type == pygame.MOUSEBUTTONUP and not end:
                if not cancel:
                    clicked = True
                    pos = pygame.mouse.get_pos()
                    if drawing and len(points) > 1:
                        drawings.append(FreehandDrawing(space, points))
                points = []
                if drawing and not cancel:
                    count += 1
                drawing = False
                cancel = False
            if event.type == pygame.MOUSEBUTTONDOWN and end:
                pos = pygame.mouse.get_pos()
                menu_condition = True
            if event.type == pygame.MOUSEMOTION and not end:
                if pygame.mouse.get_pressed()[0]:
                    points.append(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not end:
                    cancel = True

        screen.blit(permanent_surface, (0, 0))

        RestartButtonIG.draw(screen, buttons_font_IG)
        MenuButtonIG.draw(screen, buttons_font_IG)

        ball.draw(screen)

        # space.debug_draw(draw_options)

        for line in lines:
            line.draw(screen)

        for line in jar_lines:
            line.jar_draw(screen)

        if drawing and len(points) > 1 and not cancel:
            pygame.draw.lines(screen, "gray", False, points, 10)

        for drawing in drawings:
            for shape in drawing.shapes:
                start_world = drawing.body.position + \
                    shape.a.rotated(drawing.body.angle)
                end_world = drawing.body.position + \
                    shape.b.rotated(drawing.body.angle)
                pygame.draw.line(screen, "blue", start_world,
                                end_world, thickness)

        box_surface_count_live = box_font_count_live.render(
            f"Líneas dibujadas: {count}", True, [0, 0, 0])
        box_rect_count_live = box_surface_count_live.get_rect(
            center=(center_x_count_live, center_y_count_live))
        screen.blit(box_surface_count_live, box_rect_count_live)

        if ball.body.position[1] >= screen_size[1]*0.94:
            end = True
            pygame.draw.rect(screen, [255, 255, 255], (
                text_box_x, text_box_y, text_box_width, text_box_height))
            pygame.draw.rect(screen, [0, 0, 0], (
                text_box_x, text_box_y, text_box_width, text_box_height), 2)
            screen.blit(box_surface_congrats, box_rect_congrats)
            box_surface_count = box_font_count.render(
                f"Líneas dibujadas: {count}", True, [0, 0, 0])
            box_rect_count = box_surface_count.get_rect(
                center=(center_x_count, center_y_count))
            screen.blit(box_surface_count, box_rect_count)
            RestartButton.draw(screen, buttons_font)
            MenuButton.draw(screen, buttons_font)
            NextLevelButton.draw(screen, buttons_font)
            RBPos = RestartButton.position
            RBSize = RestartButton.size
            MBPos = MenuButton.position
            MBSize = MenuButton.size
            NLBPos = NextLevelButton.position
            NLBSize = NextLevelButton.size
            if menu_condition:
                if (pos[0] >= RBPos[0]) and (pos[0] <= RBPos[0] + RBSize[0]) and (pos[1] >= RBPos[1]) and (pos[1] <= RBPos[1] + RBSize[1]):
                    screen.fill("white")
                    running = False
                    quit_condition = level_1(screen, screen_size)
                elif (pos[0] >= MBPos[0]) and (pos[0] <= MBPos[0] + MBSize[0]) and (pos[1] >= MBPos[1]) and (pos[1] <= MBPos[1] + MBSize[1]):
                    screen.fill("white")
                    running = False
                    play_menu(screen, screen_size)
                elif (pos[0] >= NLBPos[0]) and (pos[0] <= NLBPos[0] + NLBSize[0]) and (pos[1] >= NLBPos[1]) and (pos[1] <= NLBPos[1] + NLBSize[1]):
                    screen.fill("white")
                    running = False
                    quit_condition = level_2(screen, screen_size)

        if clicked:
            if (pos[0] >= RIGBPos[0]) and (pos[0] <= RIGBPos[0] + RIGBSize[0]) and (pos[1] >= RIGBPos[1]) and (pos[1] <= RIGBPos[1] + RIGBSize[1]):
                screen.fill("white")
                running = False
                quit_condition = level_1(screen, screen_size)
            elif (pos[0] >= MIGBPos[0]) and (pos[0] <= MIGBPos[0] + MIGBSize[0]) and (pos[1] >= MIGBPos[1]) and (pos[1] <= MIGBPos[1] + MIGBSize[1]):
                screen.fill("white")
                running = False
                play_menu(screen, screen_size)

        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

    return quit_condition


def level_2(screen, screen_size):
    clock = pygame.time.Clock()
    FPS = 144

    space = pymunk.Space()
    space.gravity = (0, 200)

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    space.debug_draw(draw_options)

    permanent_surface = pygame.Surface(screen.get_size())
    permanent_surface.fill("white")

    drawings = []
    points = []
    drawing = False
    lines = []
    jar_lines = []
    thickness = 10
    y_scalable_constant = 175/720
    menu_condition = False
    clicked = False
    quit_condition = False
    cancel = False

    # Black Lines
    lines.append(StaticLine(space, [
                 (screen_size[0]*0.3, screen_size[1]*0.3), (screen_size[0]*0.7, screen_size[1]*0.3)], 10))
    # Limits
    lines.append(StaticLine(space, [(0, 0), (0, screen_size[1])], 1))
    lines.append(StaticLine(
        space, [(screen_size[0], 0), (screen_size[0], screen_size[1])], 1))
    lines.append(StaticLine(space, [(0, 0), (screen_size[0], 0)], 1))
    lines.append(StaticLine(
        space, [(0, screen_size[1]), (screen_size[0], screen_size[1])], 1))
    # Jar
    jar_lines.append(StaticLine(space, [
                     (screen_size[0]*(0.574-0.0390625), screen_size[1]), (screen_size[0]*(0.574-0.1171875), screen_size[1])], 5))
    jar_lines.append(StaticLine(space, [
                     (screen_size[0]*(0.574-0.0390625), screen_size[1]), (screen_size[0]*0.574, screen_size[1]*y_scalable_constant*3)], 5))
    jar_lines.append(StaticLine(space, [(screen_size[0]*(0.574-0.1171875), screen_size[1]),
                     (screen_size[0]*(0.574-0.15626), screen_size[1]*y_scalable_constant*3)], 5))
    # Ball
    ball = Ball(space, (screen_size[0]*0.5,
               screen_size[1]*0.15), screen_size[1]*0.0555555555555556)
    # Testing Ball
    #ball = Ball(space, (640, 360), screen_size[1]*0.0555555555555556)

    end, text_box_width, text_box_height, text_box_x, text_box_y, box_surface_congrats, box_rect_congrats, count, box_font_count_live, center_x_count_live, center_y_count_live, box_font_count, center_x_count, center_y_count, buttons_font, RestartButton, MenuButton, NextLevelButton = final_menu(
        screen_size)

    buttons_font_IG, RestartButtonIG, RIGBPos, RIGBSize, MenuButtonIG, MIGBPos, MIGBSize = buttons_in_game(
        screen_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_condition = True
            if event.type == pygame.MOUSEBUTTONDOWN and not end:
                if not cancel:
                    points = [event.pos]
                    drawing = True
                cancel = False
            if event.type == pygame.MOUSEBUTTONUP and not end:
                if not cancel:
                    clicked = True
                    pos = pygame.mouse.get_pos()
                    if drawing and len(points) > 1:
                        drawings.append(FreehandDrawing(space, points))
                points = []
                if drawing and not cancel:
                    count += 1
                drawing = False
                cancel = False
            if event.type == pygame.MOUSEBUTTONDOWN and end:
                pos = pygame.mouse.get_pos()
                menu_condition = True
            if event.type == pygame.MOUSEMOTION and not end:
                if pygame.mouse.get_pressed()[0]:
                    points.append(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not end:
                    cancel = True

        screen.blit(permanent_surface, (0, 0))

        RestartButtonIG.draw(screen, buttons_font_IG)
        MenuButtonIG.draw(screen, buttons_font_IG)

        ball.draw(screen)

        # space.debug_draw(draw_options)

        for line in lines:
            line.draw(screen)

        for line in jar_lines:
            line.jar_draw(screen)

        if drawing and len(points) > 1 and not cancel:
            pygame.draw.lines(screen, "gray", False, points, 10)

        for drawing in drawings:
            for shape in drawing.shapes:
                start_world = drawing.body.position + \
                    shape.a.rotated(drawing.body.angle)
                end_world = drawing.body.position + \
                    shape.b.rotated(drawing.body.angle)
                pygame.draw.line(screen, "blue", start_world,
                                end_world, thickness)

        box_surface_count_live = box_font_count_live.render(
            f"Líneas dibujadas: {count}", True, [0, 0, 0])
        box_rect_count_live = box_surface_count_live.get_rect(
            center=(center_x_count_live, center_y_count_live))
        screen.blit(box_surface_count_live, box_rect_count_live)

        if ball.body.position[1] >= screen_size[1]*0.94 and (ball.body.position[0] <= screen_size[0]*(0.574-0.0390625) and ball.body.position[0] >= screen_size[0]*(0.574-0.15626)):
            end = True
            pygame.draw.rect(screen, [255, 255, 255], (
                text_box_x, text_box_y, text_box_width, text_box_height))
            pygame.draw.rect(screen, [0, 0, 0], (
                text_box_x, text_box_y, text_box_width, text_box_height), 2)
            screen.blit(box_surface_congrats, box_rect_congrats)
            box_surface_count = box_font_count.render(
                f"Líneas dibujadas: {count}", True, [0, 0, 0])
            box_rect_count = box_surface_count.get_rect(
                center=(center_x_count, center_y_count))
            screen.blit(box_surface_count, box_rect_count)
            RestartButton.draw(screen, buttons_font)
            MenuButton.draw(screen, buttons_font)
            NextLevelButton.draw(screen, buttons_font)
            RBPos = RestartButton.position
            RBSize = RestartButton.size
            MBPos = MenuButton.position
            MBSize = MenuButton.size
            NLBPos = NextLevelButton.position
            NLBSize = NextLevelButton.size
            if menu_condition:
                if (pos[0] >= RBPos[0]) and (pos[0] <= RBPos[0] + RBSize[0]) and (pos[1] >= RBPos[1]) and (pos[1] <= RBPos[1] + RBSize[1]):
                    screen.fill("white")
                    running = False
                    quit_condition = level_2(screen, screen_size)
                elif (pos[0] >= MBPos[0]) and (pos[0] <= MBPos[0] + MBSize[0]) and (pos[1] >= MBPos[1]) and (pos[1] <= MBPos[1] + MBSize[1]):
                    screen.fill("white")
                    running = False
                    play_menu(screen, screen_size)
                elif (pos[0] >= NLBPos[0]) and (pos[0] <= NLBPos[0] + NLBSize[0]) and (pos[1] >= NLBPos[1]) and (pos[1] <= NLBPos[1] + NLBSize[1]):
                    screen.fill("white")
                    running = False
                    quit_condition = level_3(screen, screen_size)

        if clicked:
            if (pos[0] >= RIGBPos[0]) and (pos[0] <= RIGBPos[0] + RIGBSize[0]) and (pos[1] >= RIGBPos[1]) and (pos[1] <= RIGBPos[1] + RIGBSize[1]):
                screen.fill("white")
                running = False
                level_2(screen, screen_size)
            elif (pos[0] >= MIGBPos[0]) and (pos[0] <= MIGBPos[0] + MIGBSize[0]) and (pos[1] >= MIGBPos[1]) and (pos[1] <= MIGBPos[1] + MIGBSize[1]):
                screen.fill("white")
                running = False
                play_menu(screen, screen_size)

        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

    return quit_condition


def level_3(screen, screen_size):
    clock = pygame.time.Clock()
    FPS = 144

    space = pymunk.Space()
    space.gravity = (0, 200)

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    space.debug_draw(draw_options)

    permanent_surface = pygame.Surface(screen.get_size())
    permanent_surface.fill("white")

    drawings = []
    points = []
    drawing = False
    lines = []
    jar_lines = []
    spring_lines = []
    thickness = 10
    y_scalable_constant = 175/720
    menu_condition = False
    clicked = False
    quit_condition = False
    cancel = False

    # Black Lines
    lines.append(StaticLine(space, [
                (0, screen_size[1]*0.3), (screen_size[0]*0.2045, screen_size[1]*0.3)], 10))
    lines.append(StaticLine(space, [
                (screen_size[0]*0.2, screen_size[1]*0.3), (screen_size[0]*0.2, screen_size[1])], 10))
    # Spring Lines
    spring_lines.append(StaticLine(space, [
                (screen_size[0]*0.4, screen_size[1]*0.99), (screen_size[0]*0.5, screen_size[1]*0.99)], 10))
    # Limits
    lines.append(StaticLine(space, [(0, 0), (0, screen_size[1])], 1))
    lines.append(StaticLine(
        space, [(screen_size[0], 0), (screen_size[0], screen_size[1])], 1))
    lines.append(StaticLine(space, [(0, 0), (screen_size[0], 0)], 1))
    lines.append(StaticLine(
        space, [(0, screen_size[1]), (screen_size[0], screen_size[1])], 1))
    # Jar
    # jar_lines.append(StaticLine(space, [
    #                  (screen_size[0]*(0.574-0.0390625), screen_size[1]), (screen_size[0]*(0.574-0.1171875), screen_size[1])], 5))
    # jar_lines.append(StaticLine(space, [
    #                  (screen_size[0]*(0.574-0.0390625), screen_size[1]), (screen_size[0]*0.574, screen_size[1]*y_scalable_constant*3)], 5))
    # jar_lines.append(StaticLine(space, [(screen_size[0]*(0.574-0.1171875), screen_size[1]),
    #                  (screen_size[0]*(0.574-0.15626), screen_size[1]*y_scalable_constant*3)], 5))
    # Ball
    # ball = Ball(space, (screen_size[0]*0.5,
    #           screen_size[1]*0.15), screen_size[1]*0.0555555555555556)
    # Testing Ball
    ball = Ball(space, (150, 200), screen_size[1]*0.0555555555555556)

    end, text_box_width, text_box_height, text_box_x, text_box_y, box_surface_congrats, box_rect_congrats, count, box_font_count_live, center_x_count_live, center_y_count_live, box_font_count, center_x_count, center_y_count, buttons_font, RestartButton, MenuButton, NextLevelButton = final_menu(
        screen_size)

    buttons_font_IG, RestartButtonIG, RIGBPos, RIGBSize, MenuButtonIG, MIGBPos, MIGBSize = buttons_in_game(
        screen_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_condition = True
            if event.type == pygame.MOUSEBUTTONDOWN and not end:
                if not cancel:
                    points = [event.pos]
                    drawing = True
                cancel = False
            if event.type == pygame.MOUSEBUTTONUP and not end:
                if not cancel:
                    clicked = True
                    pos = pygame.mouse.get_pos()
                    if drawing and len(points) > 1:
                        drawings.append(FreehandDrawing(space, points))
                points = []
                if drawing and not cancel:
                    count += 1
                drawing = False
                cancel = False
            if event.type == pygame.MOUSEBUTTONDOWN and end:
                pos = pygame.mouse.get_pos()
                menu_condition = True
            if event.type == pygame.MOUSEMOTION and not end:
                if pygame.mouse.get_pressed()[0]:
                    points.append(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not end:
                    cancel = True

        screen.blit(permanent_surface, (0, 0))

        RestartButtonIG.draw(screen, buttons_font_IG)
        MenuButtonIG.draw(screen, buttons_font_IG)

        ball.draw(screen)

        # space.debug_draw(draw_options)

        for line in lines:
            line.draw(screen)

        for line in jar_lines:
            line.jar_draw(screen)

        if drawing and len(points) > 1 and not cancel:
            pygame.draw.lines(screen, "gray", False, points, 10)

        for drawing in drawings:
            for shape in drawing.shapes:
                start_world = drawing.body.position + \
                    shape.a.rotated(drawing.body.angle)
                end_world = drawing.body.position + \
                    shape.b.rotated(drawing.body.angle)
                pygame.draw.line(screen, "blue", start_world,
                                end_world, thickness)

        box_surface_count_live = box_font_count_live.render(
            f"Líneas dibujadas: {count}", True, [0, 0, 0])
        box_rect_count_live = box_surface_count_live.get_rect(
            center=(center_x_count_live, center_y_count_live))
        screen.blit(box_surface_count_live, box_rect_count_live)

        if ball.body.position[1] >= screen_size[1]*0.94 and (ball.body.position[0] <= screen_size[0]*(0.574-0.0390625) and ball.body.position[0] >= screen_size[0]*(0.574-0.15626)):
            end = True
            pygame.draw.rect(screen, [255, 255, 255], (
                text_box_x, text_box_y, text_box_width, text_box_height))
            pygame.draw.rect(screen, [0, 0, 0], (
                text_box_x, text_box_y, text_box_width, text_box_height), 2)
            screen.blit(box_surface_congrats, box_rect_congrats)
            box_surface_count = box_font_count.render(
                f"Líneas dibujadas: {count}", True, [0, 0, 0])
            box_rect_count = box_surface_count.get_rect(
                center=(center_x_count, center_y_count))
            screen.blit(box_surface_count, box_rect_count)
            RestartButton.position = (screen_size[0]*0.35, screen_size[1]*0.58)
            MenuButton.position = (screen_size[0]*0.6, screen_size[1]*0.58)
            RestartButton.draw(screen, buttons_font)
            MenuButton.draw(screen, buttons_font)
            RBPos = RestartButton.position
            RBSize = RestartButton.size
            MBPos = MenuButton.position
            MBSize = MenuButton.size
            if menu_condition:
                if (pos[0] >= RBPos[0]) and (pos[0] <= RBPos[0] + RBSize[0]) and (pos[1] >= RBPos[1]) and (pos[1] <= RBPos[1] + RBSize[1]):
                    screen.fill("white")
                    running = False
                    quit_condition = level_3(screen, screen_size)
                elif (pos[0] >= MBPos[0]) and (pos[0] <= MBPos[0] + MBSize[0]) and (pos[1] >= MBPos[1]) and (pos[1] <= MBPos[1] + MBSize[1]):
                    screen.fill("white")
                    running = False
                    play_menu(screen, screen_size)

        if clicked:
            if (pos[0] >= RIGBPos[0]) and (pos[0] <= RIGBPos[0] + RIGBSize[0]) and (pos[1] >= RIGBPos[1]) and (pos[1] <= RIGBPos[1] + RIGBSize[1]):
                screen.fill("white")
                running = False
                quit_condition = level_3(screen, screen_size)
            elif (pos[0] >= MIGBPos[0]) and (pos[0] <= MIGBPos[0] + MIGBSize[0]) and (pos[1] >= MIGBPos[1]) and (pos[1] <= MIGBPos[1] + MIGBSize[1]):
                screen.fill("white")
                running = False
                play_menu(screen, screen_size)

        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

    return quit_condition


def settings_menu(screen, screen_size):
    screen.fill("red")
