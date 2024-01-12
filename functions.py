import pygame
import pymunk
from classes import *
import random
import json
import pymunk.pygame_util


def print_screen(screen: pygame.Surface, screen_size: tuple[int, int]):
    """Muestra en pantalla el fondo del menú principal y lo ajusta para el tamaño de la pantalla, tambíen añade el icóno a la pantalla del juego.

    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.
    """
    pygame.display.set_caption("Fisiks")
    icon = pygame.image.load(".\\assets\\icon.png")
    pygame.display.set_icon(icon)
    bg = pygame.image.load(".\\assets\\background.png")
    bg = pygame.transform.scale(bg, (screen_size[0], screen_size[1]))
    screen.blit(bg, (0, 0))


def main_menu(screen: pygame.Surface, screen_size: tuple[int, int], enlarge: bool) -> tuple[Button, Button]:
    """Crea los botones y las cajas en el menú principal, y los dibuja en la pantalla.
    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.
        enlarge (bool): Condición de agrandar los botones o no, dependiendo si el ratón está encima del botón o no.

    Returns:
        tuple[Button, Button]: Devuelve los dos botones creados para poder acceder a sus datos más tarde.
    """
    title = "Fisiks"
    title_font_size = int(screen_size[1] * 0.12)

    buttons_font_size = int(screen_size[1] * 0.06)
    button_width = int(screen_size[0] * 0.15)
    button_height = int(screen_size[1] * 0.08)

    title_y = screen_size[1] * 0.1
    button_x = screen_size[0] * 0.05
    play_button_y = screen_size[1] * 0.42
    quit_button_y = screen_size[1] * 0.55

    title_font = pygame.font.SysFont("Calibri", title_font_size, bold=True)
    text_surface = title_font.render(title, True, [0, 0, 0])
    buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)

    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, title_y))
    screen.blit(text_surface, text_rect)  # Title

    box_width = screen_size[0] * 0.28
    box_height = screen_size[1] * 0.5
    box_x = screen_size[0] * 0.7
    box_y = screen_size[1] * 0.275

    # Draw box on the right
    pygame.draw.rect(screen, [0, 0, 0], [
                     box_x, box_y, box_width, box_height], 2)

    PlayButton = Button((button_x, play_button_y),
                        (button_width, button_height), 2, "Jugar", "black")
    QuitButton = Button((button_x, quit_button_y),
                        (button_width, button_height), 2, "Salir", "black")
    VolumeButton = Button((screen_size[0]*0.94, screen_size[1]*0.01),
                          (screen_size[0]*0.05, screen_size[1]*0.05), 0, "", "white")

    if enlarge:
        if PlayButton.is_hovered(pygame.mouse.get_pos()):
            PlayButton.draw_enlarged(screen, buttons_font)
        else:
            PlayButton.draw(screen, buttons_font)

        if QuitButton.is_hovered(pygame.mouse.get_pos()):
            QuitButton.draw_enlarged(screen, buttons_font)
        else:
            QuitButton.draw(screen, buttons_font)
    else:
        PlayButton.draw(screen, buttons_font)
        QuitButton.draw(screen, buttons_font)

    return PlayButton, QuitButton, VolumeButton


def draw_additional_ui_elements(screen: pygame.Surface, screen_size: tuple[int, int], joke_text: str, text: str):
    """Dibuja todas las partes del menú principal que no sean botones.

    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.
        joke_text (str): El texto elegido del json de los chistes.
        text (str): El texto elegido del json de los trucos.
    """
    title = "Fisiks"
    title_font_size = int(screen_size[1] * 0.12)
    title_font = pygame.font.SysFont("Calibri", title_font_size, bold=True)
    title_y = screen_size[1] * 0.1
    text_surface = title_font.render(title, True, [0, 0, 0])

    box_width = screen_size[0] * 0.28
    box_height = screen_size[1] * 0.5
    box_x = screen_size[0] * 0.7
    box_y = screen_size[1] * 0.275

    # Draw box on the right
    pygame.draw.rect(screen, [0, 0, 0], [
                     box_x, box_y, box_width, box_height], 2)

    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, title_y))
    screen.blit(text_surface, text_rect)  # Title

    title_font = pygame.font.SysFont(
        "Calibri", int(screen_size[0]*0.025), True)
    title_surface = title_font.render("Chiste", True, [0, 0, 0])
    title_rect = title_surface.get_rect(
        topleft=(screen_size[0]*(905/1280), screen_size[1]*(370/720)))
    screen.blit(title_surface, title_rect)
    wrap_text(screen, screen_size, joke_text, 0.56)
    title_font = pygame.font.SysFont(
        "Calibri", int(screen_size[0]*0.025), True)
    title_surface = title_font.render("Truco", True, [0, 0, 0])
    title_rect = title_surface.get_rect(
        topleft=(screen_size[0]*(905/1280), screen_size[1]*(210/720)))
    screen.blit(title_surface, title_rect)
    print_tips(screen, screen_size, text)


def select_joke() -> str:
    """Elige un chiste aleatorio del json. Tiene dentro un error handling por si hay algún error con el json.

    Returns:
        str: Devuelve el chiste elegido en forma de string.
    """
    try:
        with open(".\\assets\\jokes.json", "r", encoding='utf-8') as f:
            data = json.load(f)
        n = random.randint(0, len(data['jokes']) - 1)
        return data['jokes'][n]['joke']
    except FileNotFoundError:
        return "Error: Archivo no encontrado."
    except json.JSONDecodeError:
        return "Error: Formato de archivo JSON inválido."


def wrap_text(screen: pygame.Surface, screen_size: tuple[int, int], joke_text: str, y_constant: float) -> str:
    """Muestra un texto dentro de la caja, esta función hace un "textwrap", es decir, envuelve el texto para que ocupe el ancho de la caja pero no se pase y cambie de línea automaticamente. 

    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.
        joke_text (str): joke_text (str): El texto elegido del json de los chistes.
        y_constant (float): La constante del eje y, para poder situar diferentes textos en distintas alturas.
    """
    text_font = pygame.font.SysFont("Calibri", int(screen_size[0]*0.02))

    max_length = 30
    x = screen_size[0]*0.70703125
    y = screen_size[1]*y_constant
    clean_text = ""
    current_length = 0
    words = joke_text.split(" ")

    for word in words:
        current_length += len(word)
        if current_length <= (max_length) + 1:
            clean_text += word + " "
            current_length += 1
        else:
            text_surface = text_font.render(clean_text, True, [0, 0, 0])
            text_rect = text_surface.get_rect(topleft=(x, y))
            screen.blit(text_surface, text_rect)
            clean_text = ""
            current_length = 0
            clean_text += word + " "
            current_length += len(word) + 1
            y += screen_size[1]*0.035
    if clean_text.strip() != "":
        text_surface = text_font.render(clean_text, True, [0, 0, 0])
        text_rect = text_surface.get_rect(topleft=(x, y))
        screen.blit(text_surface, text_rect)


def select_tip() -> str:
    """"Elige un truco aleatorio del json. Tiene dentro un error handling por si hay algún error con el json.

    Returns:
        str: Devuelve el truco elegido en forma de string.
    """
    try:
        with open(".\\assets\\tips.json", "r", encoding='utf-8') as f:
            data = json.load(f)
        n = random.randint(0, len(data['tips']) - 1)
        return data['tips'][n]['tip']
    except FileNotFoundError:
        return "Error: Archivo no encontrado."
    except json.JSONDecodeError:
        return "Error: Formato de archivo JSON inválido."


def print_tips(screen: pygame.Surface, screen_size: tuple[int, int], text: str):
    """Cambia la constante del eje y para poder imprimir el texto de trucos en una altura distinta en la caja del menú principal.

    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.
        text (str): El texto elegido de los trucos para mostrar en pantalla.
    """
    y_constant = 0.333
    wrap_text(screen, screen_size, text, y_constant)


def play_menu(screen: pygame.Surface, screen_size: tuple[int, int], buttons_font: pygame.font.Font) -> tuple[Button, Button, Button, Button]:
    """Imprime el menú de los niveles y crea sus botones.

    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.
        buttons_font (pygame.font): El font usado para los botones en este menú.

    Returns:
        tuple[Button, Button, Button, Button]: Devuelve los botones creados para poder acceder a sus datos si fuera necesario.
    """
    # Create buttons
    button_x1, button_x2, button_x3 = screen_size[0] * \
        0.17, screen_size[0] * 0.41, screen_size[0] * 0.65
    button_width, button_height = int(
        screen_size[0] * 0.2), int(screen_size[1] * 0.1)

    Level1Button = Button(
        (button_x1, screen_size[1]*0.6), (button_width, button_height), 2, "Nivel 1", "black")
    Level2Button = Button(
        (button_x2, screen_size[1]*0.6), (button_width, button_height), 2, "Nivel 2", "black")
    Level3Button = Button(
        (button_x3, screen_size[1]*0.6), (button_width, button_height), 2, "Nivel 3", "black")
    BackButton = Button((screen_size[0]*0.01, screen_size[1]*0.01),
                        (screen_size[1]*0.1, screen_size[0]*0.03), 2, "", "black")

    for button in [Level1Button, Level2Button, Level3Button]:
        button.draw(screen, buttons_font)

    return Level1Button, Level2Button, Level3Button, BackButton


def draw_play_menu_bg(screen: pygame.Surface, screen_size: tuple[int, int]):
    """Crea las imágenes del menú de los niveles.

    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.
    """
    screen.fill("white")
    title = "Niveles"
    title_font_size = int(screen_size[1] * 0.1)
    title_y = screen_size[1] * 0.1
    title_font = pygame.font.SysFont("Calibri", title_font_size, bold=True)
    text_surface = title_font.render(title, True, [0, 0, 0])
    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, title_y))
    screen.blit(text_surface, text_rect)  # Title

    bg1 = pygame.image.load(".\\assets\\first_level.png")
    bg1 = pygame.transform.scale(bg1, (screen_size[0]*0.2, screen_size[1]*0.2))
    screen.blit(bg1, (screen_size[0] * 0.17, screen_size[1]*0.35))
    pygame.draw.rect(screen, "black", [
                     screen_size[0] * 0.17, screen_size[1]*0.35, screen_size[0]*0.2, screen_size[1]*0.203], 2)
    bg2 = pygame.image.load(".\\assets\\second_level.png")
    bg2 = pygame.transform.scale(bg2, (screen_size[0]*0.2, screen_size[1]*0.2))
    screen.blit(bg2, (screen_size[0] * 0.41, screen_size[1]*0.35))
    pygame.draw.rect(screen, "black", [
                     screen_size[0] * 0.41, screen_size[1]*0.35, screen_size[0]*0.2, screen_size[1]*0.203], 2)
    bg3 = pygame.image.load(".\\assets\\third_level.png")
    bg3 = pygame.transform.scale(bg3, (screen_size[0]*0.2, screen_size[1]*0.2))
    screen.blit(bg3, (screen_size[0] * 0.65, screen_size[1]*0.35))
    pygame.draw.rect(screen, "black", [
                     screen_size[0] * 0.65, screen_size[1]*0.35, screen_size[0]*0.2, screen_size[1]*0.203], 2)
    back = pygame.image.load(".\\assets\\home.png")
    back = pygame.transform.scale(
        back, (screen_size[0]*0.06, screen_size[1]*0.08))
    screen.blit(back, (0, 0))

    score_font_size = int(screen_size[1] * 0.05)
    score_font = pygame.font.SysFont("Calibri", score_font_size)

    try:
        with open(".\\assets\\high_scores.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            length = len(data['scores'])
    except FileNotFoundError:
        return "Error: Archivo no encontrado."
    except json.JSONDecodeError:
        return "Error: Formato de archivo JSON inválido."

    for n in range(length):
        if data['scores'][n]['score'] == 0:
            score = "No intentado"
            score_surface = score_font.render(score, True, [0, 0, 0])
            score_rect = score_surface.get_rect(
                center=(screen_size[0] * (0.27 + 0.24*n), screen_size[1]*0.3))
            screen.blit(score_surface, score_rect)
        else:
            score = f"Best Score: {data['scores'][n]['score']}"
            score_surface = score_font.render(score, True, [0, 0, 0])
            score_rect = score_surface.get_rect(
                center=(screen_size[0] * (0.27 + 0.24*n), screen_size[1]*0.3))
            screen.blit(score_surface, score_rect)


def buttons_in_game(screen_size: tuple[int, int]) -> tuple[pygame.font.Font, Button, tuple[float, float], tuple[float, float], Button, tuple[float, float], tuple[float, float]]:
    """Crea los botones en el menú de los niveles.

    Args:
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.

    Returns:
        tuple[pygame.font.Font, Button, tuple[float, float], tuple[float, float], Button, tuple[float, float], tuple[float, float]]: Devuelve el font de los botones, unos botones y unas posiciones y tamaños de botones.
    """
    buttons_font_size_IG = int(screen_size[1] * 0.06)
    buttons_font_IG = pygame.font.SysFont(
        "Calibri", buttons_font_size_IG, True)
    # Restart Button
    RestartButtonIG = Button((screen_size[0]*0.06, screen_size[1]*0.005),
                             (screen_size[0]*0.05, screen_size[1]*0.05), 1, "R", "black")
    RIGBPos = RestartButtonIG.position
    RIGBSize = RestartButtonIG.size
    # Menu Button
    MenuButtonIG = Button((screen_size[0]*0.005, screen_size[1]*0.005),
                          (screen_size[0]*0.05, screen_size[1]*0.05), 1, "M", "black")
    MIGBPos = MenuButtonIG.position
    MIGBSize = MenuButtonIG.size
    return buttons_font_IG, RestartButtonIG, RIGBPos, RIGBSize, MenuButtonIG, MIGBPos, MIGBSize


def final_menu(screen_size: tuple[int, int]) -> tuple[bool, int, int, int, int, pygame.surface.Surface, pygame.rect.Rect, int, pygame.font.Font, float, float, pygame.font.Font, float, pygame.font.Font, Button, Button, Button]:
    """Muestra el menú tras haber ganado un nivel.

    Args:
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.

    Returns:
        tuple[bool, int, int, int, int, pygame.surface.Surface, pygame.rect.Rect, int, pygame.font.Font, float, float, pygame.font.Font, float, pygame.font.Font, Button, Button, Button]: Devuelve unas condiciones y datos necesarios para la lógica del juego en el main. Tambíen devuelve unos botones y fonts.
    """
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
                           (screen_size[0]*0.15, screen_size[1]*0.1), 1, "Reiniciar", "black")
    # Menu Button
    MenuButton = Button((screen_size[0]*0.45, screen_size[1]*0.58),
                        (screen_size[0]*0.1, screen_size[1]*0.1), 1, "Menú", "black")
    # Next Level Button
    NextLevelButton = Button((screen_size[0]*0.58, screen_size[1]*0.58),
                             (screen_size[0]*0.15, screen_size[1]*0.1), 1, "Siguiente", "black")
    return end, text_box_width, text_box_height, text_box_x, text_box_y, box_surface_congrats, box_rect_congrats, count, box_font_count_live, center_x_count_live, center_y_count_live, box_font_count, center_x_count, center_y_count, buttons_font, RestartButton, MenuButton, NextLevelButton


def level_1(screen: pygame.Surface, screen_size: tuple[int, int]) -> bool:
    """Creación del nivel 1 y su lógica.

    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.

    Returns:
        bool: Devuelve una condición para decidir si el main debe cerrar el juego o no.
    """
    clock = pygame.time.Clock()
    FPS = 144

    space = pymunk.Space()
    space.gravity = (0, 200)

    permanent_surface = pygame.Surface(screen.get_size())
    permanent_surface.fill("white")

    buttons_font_size = int(screen_size[1] * 0.06)
    buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)

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
    count_condition = False

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
    lines.append(StaticLine(space, [(-500, 0), (-500, screen_size[1])], 1000))
    lines.append(StaticLine(
        space, [(500+screen_size[0], 0), (500+screen_size[0], screen_size[1])], 1000))
    lines.append(StaticLine(space, [(0, -500), (screen_size[0], -500)], 1000))
    lines.append(StaticLine(
        space, [(0, 500+screen_size[1]), (screen_size[0], 500+screen_size[1])], 1000))
    # Jar
    jar_lines.append(StaticLine(space, [
                     (screen_size[0]*0.0390625, screen_size[1]), (screen_size[0]*0.1171875, screen_size[1])], 5))
    jar_lines.append(StaticLine(space, [
                     (screen_size[0]*0.0390625, screen_size[1]), (0, screen_size[1]*y_scalable_constant*3)], 5))
    jar_lines.append(StaticLine(space, [(screen_size[0]*0.1171875, screen_size[1]),
                     (screen_size[0]*0.15625, screen_size[1]*y_scalable_constant*3)], 5))
    # Ball
    ball = Ball(space, (screen_size[0]*0.9, screen_size[1]
                        * 0.12), screen_size[1]*0.0555555555555556)
    # Testing Ball
    # ball = Ball(space, (100, 400), screen_size[1]*0.0555555555555556)

    end, text_box_width, text_box_height, text_box_x, text_box_y, box_surface_congrats, box_rect_congrats, count, box_font_count_live, center_x_count_live, center_y_count_live, box_font_count, center_x_count, center_y_count, buttons_font, RestartButton, MenuButton, NextLevelButton = final_menu(
        screen_size)

    buttons_font_IG, RestartButtonIG, RIGBPos, RIGBSize, MenuButtonIG, MIGBPos, MIGBSize = buttons_in_game(
        screen_size)

    restart = pygame.image.load(".\\assets\\reset.png")
    restart = pygame.transform.scale(
        restart, (screen_size[0]*0.05, screen_size[1]*0.05))
    permanent_surface.blit(
        restart, (screen_size[0]*0.059375, screen_size[1]*0.0041666666666667))
    menu = pygame.image.load(".\\assets\\menu.png")
    menu = pygame.transform.scale(
        menu, (screen_size[0]*0.06, screen_size[1]*0.06))

    permanent_surface.blit(menu, (0, 0))

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
                        count_condition = True
                points = []
                if event.button == 1 and count_condition and drawing and not cancel:
                    count += 1
                drawing = False
                cancel = False
                count_condition = False
            if event.type == pygame.MOUSEBUTTONUP and end:
                pos = pygame.mouse.get_pos()
                menu_condition = True
            if event.type == pygame.MOUSEMOTION and not end:
                if pygame.mouse.get_pressed()[0]:
                    points.append(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not end:
                    cancel = True
            if event.type == pygame.MOUSEMOTION and end:
                for button in [RestartButton, MenuButton, NextLevelButton]:
                    if button.update_hover(pygame.mouse.get_pos()):
                        hover_changed = True

        screen.blit(permanent_surface, (0, 0))

        if end and (ball.body.position[1] >= screen_size[1]*0.95):
            ball.draw(permanent_surface)
        else:
            ball.draw(screen)

        for line in lines:
            line.draw(permanent_surface)

        for line in jar_lines:
            line.jar_draw(permanent_surface)

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

        if end:
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

        box_surface_count_live = box_font_count_live.render(
            f"Líneas dibujadas: {count}", True, [0, 0, 0])
        box_rect_count_live = box_surface_count_live.get_rect(
            center=(center_x_count_live, center_y_count_live))
        screen.blit(box_surface_count_live, box_rect_count_live)

        if ball.body.position[1] >= screen_size[1]*0.92:
            end = True
            RBPos = RestartButton.position
            RBSize = RestartButton.size
            MBPos = MenuButton.position
            MBSize = MenuButton.size
            NLBPos = NextLevelButton.position
            NLBSize = NextLevelButton.size
            if end:
                for button in [RestartButton, MenuButton, NextLevelButton]:
                    if button.hovered:
                        button.draw_enlarged(screen, buttons_font)
                    else:
                        button.draw(screen, buttons_font)
                pygame.display.flip()
                if menu_condition:
                    if (pos[0] >= RBPos[0]) and (pos[0] <= RBPos[0] + RBSize[0]) and (pos[1] >= RBPos[1]) and (pos[1] <= RBPos[1] + RBSize[1]):
                        screen.fill("white")
                        running = False
                        quit_condition = level_1(screen, screen_size)
                    elif (pos[0] >= MBPos[0]) and (pos[0] <= MBPos[0] + MBSize[0]) and (pos[1] >= MBPos[1]) and (pos[1] <= MBPos[1] + MBSize[1]):
                        screen.fill("white")
                        running = False
                        play_menu(screen, screen_size, buttons_font)
                    elif (pos[0] >= NLBPos[0]) and (pos[0] <= NLBPos[0] + NLBSize[0]) and (pos[1] >= NLBPos[1]) and (pos[1] <= NLBPos[1] + NLBSize[1]):
                        screen.fill("white")
                        running = False
                        quit_condition = level_2(screen, screen_size)

                    n = 0
                    with open(".\\assets\\high_scores.json", "r", encoding='utf-8') as f:
                        data = json.load(f)

                    data['scores'][n]['score'] = count

                    with open(".\\assets\\high_scores.json", "w", encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)

        if clicked:
            if (pos[0] >= RIGBPos[0]) and (pos[0] <= RIGBPos[0] + RIGBSize[0]) and (pos[1] >= RIGBPos[1]) and (pos[1] <= RIGBPos[1] + RIGBSize[1]):
                screen.fill("white")
                running = False
                quit_condition = level_1(screen, screen_size)
            elif (pos[0] >= MIGBPos[0]) and (pos[0] <= MIGBPos[0] + MIGBSize[0]) and (pos[1] >= MIGBPos[1]) and (pos[1] <= MIGBPos[1] + MIGBSize[1]):
                screen.fill("white")
                running = False
                play_menu(screen, screen_size, buttons_font)

        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

    return quit_condition


def level_2(screen: pygame.Surface, screen_size: tuple[int, int]) -> bool:
    """Creación del nivel 2 y su lógica.

    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.

    Returns:
        bool: Devuelve una condición para decidir si el main debe cerrar el juego o no.
    """
    clock = pygame.time.Clock()
    FPS = 144

    space = pymunk.Space()
    space.gravity = (0, 200)

    # draw_options = pymunk.pygame_util.DrawOptions(screen)
    # space.debug_draw(draw_options)

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
    count_condition = False

    # Black Lines
    lines.append(StaticLine(space, [
                 (screen_size[0]*0.3, screen_size[1]*0.3), (screen_size[0]*0.7, screen_size[1]*0.3)], 10))
    # Limits
    lines.append(StaticLine(space, [(-500, 0), (-500, screen_size[1])], 1000))
    lines.append(StaticLine(
        space, [(500+screen_size[0], 0), (500+screen_size[0], screen_size[1])], 1000))
    lines.append(StaticLine(space, [(0, -500), (screen_size[0], -500)], 1000))
    lines.append(StaticLine(
        space, [(0, 500+screen_size[1]), (screen_size[0], 500+screen_size[1])], 1000))
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
    # ball = Ball(space, (640, 360), screen_size[1]*0.0555555555555556)

    end, text_box_width, text_box_height, text_box_x, text_box_y, box_surface_congrats, box_rect_congrats, count, box_font_count_live, center_x_count_live, center_y_count_live, box_font_count, center_x_count, center_y_count, buttons_font, RestartButton, MenuButton, NextLevelButton = final_menu(
        screen_size)

    buttons_font_IG, RestartButtonIG, RIGBPos, RIGBSize, MenuButtonIG, MIGBPos, MIGBSize = buttons_in_game(
        screen_size)

    restart = pygame.image.load(".\\assets\\reset.png")
    restart = pygame.transform.scale(
        restart, (screen_size[0]*0.05, screen_size[1]*0.05))
    permanent_surface.blit(
        restart, (screen_size[0]*0.059375, screen_size[1]*0.0041666666666667))
    menu = pygame.image.load(".\\assets\\menu.png")
    menu = pygame.transform.scale(
        menu, (screen_size[0]*0.06, screen_size[1]*0.06))
    permanent_surface.blit(menu, (0, 0))

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
                        count_condition = True
                points = []
                if event.button == 1 and count_condition and drawing and not cancel:
                    count += 1
                drawing = False
                cancel = False
                count_condition = False
            if event.type == pygame.MOUSEBUTTONUP and end:
                pos = pygame.mouse.get_pos()
                menu_condition = True
            if event.type == pygame.MOUSEMOTION and not end:
                if pygame.mouse.get_pressed()[0]:
                    points.append(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not end:
                    cancel = True
            if event.type == pygame.MOUSEMOTION and end:
                for button in [RestartButton, MenuButton, NextLevelButton]:
                    if button.update_hover(pygame.mouse.get_pos()):
                        hover_changed = True

        screen.blit(permanent_surface, (0, 0))

        if end and ball.body.position[1] >= screen_size[1]*0.95:
            ball.draw(permanent_surface)
        else:
            ball.draw(screen)

        # space.debug_draw(draw_options)

        for line in lines:
            line.draw(permanent_surface)

        for line in jar_lines:
            line.jar_draw(permanent_surface)

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

        if end:
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

        box_surface_count_live = box_font_count_live.render(
            f"Líneas dibujadas: {count}", True, [0, 0, 0])
        box_rect_count_live = box_surface_count_live.get_rect(
            center=(center_x_count_live, center_y_count_live))
        screen.blit(box_surface_count_live, box_rect_count_live)

        if ball.body.position[1] <= screen_size[1] and ball.body.position[1] >= screen_size[1]*0.9 and (ball.body.position[0] <= screen_size[0]*(0.574-0.0390625) and ball.body.position[0] >= screen_size[0]*(0.574-0.15626)):
            end = True
            RBPos = RestartButton.position
            RBSize = RestartButton.size
            MBPos = MenuButton.position
            MBSize = MenuButton.size
            NLBPos = NextLevelButton.position
            NLBSize = NextLevelButton.size
            if end:
                for button in [RestartButton, MenuButton, NextLevelButton]:
                    if button.hovered:
                        button.draw_enlarged(screen, buttons_font)
                    else:
                        button.draw(screen, buttons_font)
                pygame.display.flip()
                if menu_condition:
                    if (pos[0] >= RBPos[0]) and (pos[0] <= RBPos[0] + RBSize[0]) and (pos[1] >= RBPos[1]) and (pos[1] <= RBPos[1] + RBSize[1]):
                        screen.fill("white")
                        permanent_surface.fill("white")
                        running = False
                        quit_condition = level_2(screen, screen_size)
                    elif (pos[0] >= MBPos[0]) and (pos[0] <= MBPos[0] + MBSize[0]) and (pos[1] >= MBPos[1]) and (pos[1] <= MBPos[1] + MBSize[1]):
                        screen.fill("white")
                        permanent_surface.fill("white")
                        running = False
                        play_menu(screen, screen_size, buttons_font)
                    elif (pos[0] >= NLBPos[0]) and (pos[0] <= NLBPos[0] + NLBSize[0]) and (pos[1] >= NLBPos[1]) and (pos[1] <= NLBPos[1] + NLBSize[1]):
                        screen.fill("white")
                        permanent_surface.fill("white")
                        running = False
                        quit_condition = level_3(screen, screen_size)

                    n = 1
                    with open(".\\assets\\high_scores.json", "r", encoding='utf-8') as f:
                        data = json.load(f)

                    data['scores'][n]['score'] = count

                    with open(".\\assets\\high_scores.json", "w", encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)

        if clicked:
            if (pos[0] >= RIGBPos[0]) and (pos[0] <= RIGBPos[0] + RIGBSize[0]) and (pos[1] >= RIGBPos[1]) and (pos[1] <= RIGBPos[1] + RIGBSize[1]):
                screen.fill("white")
                permanent_surface.fill("white")
                running = False
                level_2(screen, screen_size)
            elif (pos[0] >= MIGBPos[0]) and (pos[0] <= MIGBPos[0] + MIGBSize[0]) and (pos[1] >= MIGBPos[1]) and (pos[1] <= MIGBPos[1] + MIGBSize[1]):
                screen.fill("white")
                permanent_surface.fill("white")
                running = False
                play_menu(screen, screen_size, buttons_font)

        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

    return quit_condition


def level_3(screen: pygame.Surface, screen_size: tuple[int, int]) -> bool:
    """Creación del nivel 3 y su lógica.

    Args:
        screen (pygame.Surface): La pantalla del juego.
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.

    Returns:
        bool: Devuelve una condición para decidir si el main debe cerrar el juego o no.
    """
    clock = pygame.time.Clock()
    FPS = 144

    space = pymunk.Space()
    space.gravity = (0, 200)

    permanent_surface = pygame.Surface(screen.get_size())
    permanent_surface.fill("white")

    drawings = []
    points = []
    drawing = False
    lines = []
    jar_lines = []
    spring_lines_floor = []
    spring_lines_wall = []
    thickness = 10
    y_scalable_constant = 175/720
    menu_condition = False
    clicked = False
    quit_condition = False
    cancel = False
    count_condition = False

    # Black Lines
    lines.append(StaticLine(space, [
                (0, screen_size[1]*0.25), (screen_size[0]*0.2045, screen_size[1]*0.25)], 10))
    lines.append(StaticLine(space, [
                (screen_size[0]*0.2, screen_size[1]*0.25), (screen_size[0]*0.2, screen_size[1]*0.35)], 10))
    lines.append(StaticLine(space, [
                (0, screen_size[1]*0.35), (screen_size[0]*0.2045, screen_size[1]*0.35)], 10))
    lines.append(StaticLine(space, [
                (0, screen_size[1]*0.9), (screen_size[0]*0.2045, screen_size[1]*0.9)], 10))
    lines.append(StaticLine(space, [
                (screen_size[0]*0.2, screen_size[1]*0.9), (screen_size[0]*0.2, screen_size[1])], 10))
    lines.append(StaticLine(space, [
                (screen_size[0]*0.15, screen_size[1]*0.35), (0, screen_size[1]*0.6)], 10))
    lines.append(StaticLine(space, [
                (screen_size[0]*0.685, screen_size[1]*0.3), (screen_size[0]*0.685, screen_size[1])], 10))
    lines.append(StaticLine(space, [
                (screen_size[0]*0.6815, screen_size[1]*0.3), (screen_size[0], screen_size[1]*0.3)], 10))
    # Spring Lines
    spring_floor = (StaticLine(space, [
        (screen_size[0]*0.4, screen_size[1]*0.99), (screen_size[0]*0.5, screen_size[1]*0.99)], 10))
    spring_wall = (StaticLine(space, [
        (screen_size[0]*0.678, screen_size[1]*0.5), (screen_size[0]*0.678, screen_size[1]*0.7)], 10))
    spring_lines_floor.append(spring_floor)
    spring_lines_wall.append(spring_wall)
    # Limits
    lines.append(StaticLine(space, [(0, 0), (0, screen_size[1])], 1))
    lines.append(StaticLine(
        space, [(screen_size[0], 0), (screen_size[0], screen_size[1])], 1))
    lines.append(StaticLine(space, [(0, 0), (screen_size[0], 0)], 1))
    lines.append(StaticLine(
        space, [(0, screen_size[1]), (screen_size[0], screen_size[1])], 1))
    # Jar
    Jar = (StaticLine(space, [
                     (screen_size[0]*(0.18-0.0390625), screen_size[1]*0.89), (screen_size[0]*(0.18-0.1171875), screen_size[1]*0.89)], 5))
    jar_lines.append(Jar)
    jar_lines.append(StaticLine(space, [
                     (screen_size[0]*(0.18-0.0390625), screen_size[1]*0.89), (screen_size[0]*0.18, screen_size[1]*y_scalable_constant*3*0.89)], 5))
    jar_lines.append(StaticLine(space, [(screen_size[0]*(0.18-0.1171875), screen_size[1]*0.89),
                     (screen_size[0]*(0.18-0.15626), screen_size[1]*y_scalable_constant*3*0.89)], 5))
    # Ball
    ball = Ball(space, (screen_size[0]*0.1, screen_size[1]
                * 0.1), screen_size[1]*0.0555555555555556)
    # Testing Ball
    # ball = Ball(space, (150, 300), screen_size[1]*0.0555555555555556)

    end, text_box_width, text_box_height, text_box_x, text_box_y, box_surface_congrats, box_rect_congrats, count, box_font_count_live, center_x_count_live, center_y_count_live, box_font_count, center_x_count, center_y_count, buttons_font, RestartButton, MenuButton, NextLevelButton = final_menu(
        screen_size)

    buttons_font_IG, RestartButtonIG, RIGBPos, RIGBSize, MenuButtonIG, MIGBPos, MIGBSize = buttons_in_game(
        screen_size)

    restart = pygame.image.load(".\\assets\\reset.png")
    restart = pygame.transform.scale(
        restart, (screen_size[0]*0.05, screen_size[1]*0.05))
    permanent_surface.blit(
        restart, (screen_size[0]*0.059375, screen_size[1]*0.0041666666666667))
    menu = pygame.image.load(".\\assets\\menu.png")
    menu = pygame.transform.scale(
        menu, (screen_size[0]*0.06, screen_size[1]*0.06))
    permanent_surface.blit(menu, (0, 0))

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
                        count_condition = True
                points = []
                if event.button == 1 and count_condition and drawing and not cancel:
                    count += 1
                drawing = False
                cancel = False
                count_condition = False
            if event.type == pygame.MOUSEBUTTONUP and end:
                pos = pygame.mouse.get_pos()
                menu_condition = True
            if event.type == pygame.MOUSEMOTION and not end:
                if pygame.mouse.get_pressed()[0]:
                    points.append(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not end:
                    cancel = True
            if event.type == pygame.MOUSEMOTION and end:
                for button in [RestartButton, MenuButton, NextLevelButton]:
                    if button.update_hover(pygame.mouse.get_pos()):
                        hover_changed = True

        screen.blit(permanent_surface, (0, 0))

        if end and (ball.body.position[1] >= screen_size[1]*0.84 and ball.body.position[1] <= screen_size[1]*0.9):
            ball.draw(permanent_surface)
        else:
            ball.draw(screen)

        for line in lines:
            line.draw(permanent_surface)

        for line in jar_lines:
            line.jar_draw(permanent_surface)

        for spring in spring_lines_floor:
            spring.spring_draw_floor(permanent_surface)

        for spring in spring_lines_wall:
            spring.spring_draw_wall(permanent_surface)

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

        if end:
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
            RestartButton.position = (screen_size[0]*0.37, screen_size[1]*0.58)
            MenuButton.position = (screen_size[0]*0.53, screen_size[1]*0.58)
            RestartButton.draw(screen, buttons_font)
            MenuButton.draw(screen, buttons_font)

        box_surface_count_live = box_font_count_live.render(
            f"Líneas dibujadas: {count}", True, [0, 0, 0])
        box_rect_count_live = box_surface_count_live.get_rect(
            center=(center_x_count_live, center_y_count_live))
        screen.blit(box_surface_count_live, box_rect_count_live)

        if (ball.body.position[1] >= screen_size[1]*0.8 and ball.body.position[1] <= screen_size[1]*0.9) and (ball.body.position[0] <= screen_size[0]*(0.18-0.0390625) and ball.body.position[0] >= screen_size[0]*(0.18-0.15626)):
            end = True
            RBPos = RestartButton.position
            RBSize = RestartButton.size
            MBPos = MenuButton.position
            MBSize = MenuButton.size
            if end:
                for button in [RestartButton, MenuButton]:
                    if button.hovered:
                        button.draw_enlarged(screen, buttons_font)
                    else:
                        button.draw(screen, buttons_font)
                pygame.display.flip()
                if menu_condition:
                    if (pos[0] >= RBPos[0]) and (pos[0] <= RBPos[0] + RBSize[0]) and (pos[1] >= RBPos[1]) and (pos[1] <= RBPos[1] + RBSize[1]):
                        screen.fill("white")
                        permanent_surface.fill("white")
                        running = False
                        quit_condition = level_3(screen, screen_size)
                    elif (pos[0] >= MBPos[0]) and (pos[0] <= MBPos[0] + MBSize[0]) and (pos[1] >= MBPos[1]) and (pos[1] <= MBPos[1] + MBSize[1]):
                        screen.fill("white")
                        permanent_surface.fill("white")
                        running = False
                        play_menu(screen, screen_size, buttons_font)

                    n = 2
                    with open(".\\assets\\high_scores.json", "r", encoding='utf-8') as f:
                        data = json.load(f)

                    data['scores'][n]['score'] = count

                    with open(".\\assets\\high_scores.json", "w", encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)

        if clicked:
            if (pos[0] >= RIGBPos[0]) and (pos[0] <= RIGBPos[0] + RIGBSize[0]) and (pos[1] >= RIGBPos[1]) and (pos[1] <= RIGBPos[1] + RIGBSize[1]):
                screen.fill("white")
                permanent_surface.fill("white")
                running = False
                quit_condition = level_3(screen, screen_size)
            elif (pos[0] >= MIGBPos[0]) and (pos[0] <= MIGBPos[0] + MIGBSize[0]) and (pos[1] >= MIGBPos[1]) and (pos[1] <= MIGBPos[1] + MIGBSize[1]):
                screen.fill("white")
                permanent_surface.fill("white")
                running = False
                play_menu(screen, screen_size, buttons_font)

        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

    return quit_condition


def choose_resolution(screen_size: tuple[int, int]) -> tuple[Button, Button, Button, Button, Button, Button]:
    """El menú para elegir la resolución del juego.

    Args:
        screen_size (tuple[int, int]): El tamaño de la pantalla del juego.

    Returns:
        tuple[Button, Button, Button, Button, Button, Button]: Devuelve unos botones para luego aplicarlos en la lógica del menú.
    """
    # Change Resolution Button
    ChangeResolutionButton = Button((screen_size[0]*0.38, screen_size[1]*0.8),
                                    (screen_size[0]*0.25, screen_size[1]*0.1), 1, "Aplicar Cambios", "black")
    # Resolution Buttons
    Res1Button = Button((screen_size[0]*0.425, screen_size[1]*0.25),
                        (screen_size[0]*0.15, screen_size[1]*0.08), 1, "1920x1080", "black")
    Res2Button = Button((screen_size[0]*0.425, screen_size[1]*0.35),
                        (screen_size[0]*0.15, screen_size[1]*0.08), 1, "1280x720", "black")

    Res3Button = Button((screen_size[0]*0.425, screen_size[1]*0.52),
                        (screen_size[0]*0.15, screen_size[1]*0.08), 1, "1920x1200", "black")
    Res4Button = Button((screen_size[0]*0.425, screen_size[1]*0.62),
                        (screen_size[0]*0.15, screen_size[1]*0.08), 1, "1280x800", "black")
    return ChangeResolutionButton, Res1Button, Res2Button, Res3Button, Res4Button


def choose_resolution_screen() -> tuple[bool, tuple[int, int]]:
    """Imprime la pantalla para el menú de elegir la resolución.

    Returns:
        tuple[bool, tuple[int, int]]: Devuelve una condición para cerrar el juego y el tamaño de la pantalla elegido.
    """
    screen_size_cr = (1280, 720)
    screen_size = screen_size_cr
    screen = pygame.display.set_mode((screen_size_cr[0], screen_size_cr[1]))
    icon = pygame.image.load(".\\assets\\icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Fisiks - Resolution Screen")
    screen.fill("white")
    ChangeResolutionButton, Res1Button, Res2Button, Res3Button, Res4Button = choose_resolution(
        screen_size_cr)
    CRBPos = ChangeResolutionButton.position
    CRBSize = ChangeResolutionButton.size
    R1BPos = Res1Button.position
    R1BSize = Res1Button.size
    R2BPos = Res2Button.position
    R2BSize = Res2Button.size
    R3BPos = Res3Button.position
    R3BSize = Res3Button.size
    R4BPos = Res4Button.position
    R4BSize = Res4Button.size

    change_res_font_size = int(screen_size_cr[1] * 0.06)
    change_res_font = pygame.font.SysFont("Calibri", change_res_font_size)
    buttons_font_size = int(screen_size_cr[1] * 0.05)
    buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)

    quit_game = False
    running = True
    while running:
        pos = (0, 0)
        hover_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ChangeResolutionButton.is_hovered(event.pos):
                    ChangeResolutionButton.draw_enlarged(
                        screen, change_res_font)
                elif Res1Button.is_hovered(event.pos):
                    Res1Button.draw_enlarged(screen, buttons_font)
                elif Res2Button.is_hovered(event.pos):
                    Res2Button.draw_enlarged(screen, buttons_font)
                elif Res3Button.is_hovered(event.pos):
                    Res3Button.draw_enlarged(screen, buttons_font)
                elif Res4Button.is_hovered(event.pos):
                    Res4Button.draw_enlarged(screen, buttons_font)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEMOTION:
                for button in [ChangeResolutionButton, Res1Button, Res2Button, Res3Button, Res4Button]:
                    if button.update_hover(hover_pos):
                        hover_changed = True

        screen.fill("white")
        resolution_font_size = int(screen_size[1] * 0.09)
        resolution_font = pygame.font.SysFont(
            "Calibri", resolution_font_size, bold=True)
        resolution_surface = resolution_font.render(
            "Resolución", True, [0, 0, 0])
        resolution_rect = resolution_surface.get_rect(
            center=(screen_size[0]*0.5, screen_size[1]*0.1))
        screen.blit(resolution_surface, resolution_rect)
        ar_font_size = int(screen_size[1] * 0.05)
        ar_font = pygame.font.SysFont("Calibri", ar_font_size, bold=True)
        ar_surface = ar_font.render("16:9", True, [0, 0, 0])
        ar_rect = ar_surface.get_rect(
            center=(screen_size[0]*0.5, screen_size[1]*0.21))
        screen.blit(ar_surface, ar_rect)
        ar_font = pygame.font.SysFont("Calibri", ar_font_size, bold=True)
        ar_surface = ar_font.render("16:10", True, [0, 0, 0])
        ar_rect = ar_surface.get_rect(
            center=(screen_size[0]*0.5, screen_size[1]*0.48))
        screen.blit(ar_surface, ar_rect)
        if not ChangeResolutionButton.hovered:
            ChangeResolutionButton.draw(screen, change_res_font)
        else:
            ChangeResolutionButton.draw_enlarged(
                screen, change_res_font)
        if not Res1Button.hovered:
            Res1Button.draw(screen, buttons_font)
        else:
            Res1Button.draw_enlarged(screen, buttons_font)
        if not Res2Button.hovered:
            Res2Button.draw(screen, buttons_font)
        else:
            Res2Button.draw_enlarged(screen, buttons_font)
        if not Res3Button.hovered:
            Res3Button.draw(screen, buttons_font)
        else:
            Res3Button.draw_enlarged(screen, buttons_font)
        if not Res4Button.hovered:
            Res4Button.draw(screen, buttons_font)
        else:
            Res4Button.draw_enlarged(screen, buttons_font)

        # Handle resolution change logic
        if (pos[0] >= R1BPos[0]) and (pos[0] <= R1BPos[0] + R1BSize[0]) and (pos[1] >= R1BPos[1]) and (pos[1] <= R1BPos[1] + R1BSize[1]):
            screen_size_cr = (1920, 1080)
            Res1Button.colour = "orange"
            for button in [Res2Button, Res3Button, Res4Button]:
                button.colour = "black"
        elif (pos[0] >= R2BPos[0]) and (pos[0] <= R2BPos[0] + R2BSize[0]) and (pos[1] >= R2BPos[1]) and (pos[1] <= R2BPos[1] + R2BSize[1]):
            screen_size_cr = (1280, 720)
            Res2Button.colour = "orange"
            for button in [Res1Button, Res3Button, Res4Button]:
                button.colour = "black"
        elif (pos[0] >= R3BPos[0]) and (pos[0] <= R3BPos[0] + R3BSize[0]) and (pos[1] >= R3BPos[1]) and (pos[1] <= R3BPos[1] + R3BSize[1]):
            screen_size_cr = (1920, 1200)
            Res3Button.colour = "orange"
            for button in [Res1Button, Res2Button, Res4Button]:
                button.colour = "black"
        elif (pos[0] >= R4BPos[0]) and (pos[0] <= R4BPos[0] + R4BSize[0]) and (pos[1] >= R4BPos[1]) and (pos[1] <= R4BPos[1] + R4BSize[1]):
            screen_size_cr = (1280, 800)
            Res4Button.colour = "orange"
            for button in [Res1Button, Res2Button, Res3Button]:
                button.colour = "black"
        if (pos[0] >= CRBPos[0]) and (pos[0] <= CRBPos[0] + CRBSize[0]) and (pos[1] >= CRBPos[1]) and (pos[1] <= CRBPos[1] + CRBSize[1]):
            running = False

        pygame.display.flip()

    return quit_game, screen_size_cr


def check_json() -> str:
    try:
        with open(".\\assets\\high_scores.json", "r", encoding='utf-8') as f:
            data = json.load(f)

        if data['local_load'][0]['times'] == 0:
            for n in range(len(data['scores'])):
                data['scores'][n]['score'] = 0
                with open(".\\assets\\high_scores.json", "w", encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            data['local_load'][0]['times'] = 1
            with open(".\\assets\\high_scores.json", "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            data['local_load'][0]['times'] += 1
            with open(".\\assets\\high_scores.json", "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        return "Error: Archivo no encontrado."
    except json.JSONDecodeError:
        return "Error: Formato de archivo JSON inválido."
