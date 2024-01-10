import functions as f
import pygame

game = False
quit_game = False

pygame.init()
quit_game, screen_size = f.choose_resolution_screen()
pygame.quit()


if not quit_game:
    pygame.init()

    pygame.mixer.init()
    pygame.mixer.music.load('.\\assets\\music.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)

    screen = pygame.display.set_mode((screen_size[0], screen_size[1]))

    buttons_font_size = int(screen_size[1] * 0.06)
    buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)

    f.print_screen(screen, screen_size)

    box_font_size = int(screen_size[1] * 0.04)
    box_font = pygame.font.SysFont("Calibri", box_font_size)
    text_box_width = int(screen_size[0] * 0.10)
    text_box_height = int(screen_size[1] * 0.2)

    text_box_x = screen_size[0] * 0.8
    text_box_y = screen_size[1] * 0.5

    joke_text = f.select_joke()
    text = f.select_tip()

    enlarge = False
    PlayButton, QuitButton = f.main_menu(
        screen, screen_size, enlarge)
    f.draw_additional_ui_elements(screen, screen_size, joke_text, text)
    PBSize = PlayButton.size
    PBPos = PlayButton.position
    QBSize = QuitButton.size
    QBPos = QuitButton.position
    buttons_font_size = int(screen_size[1] * 0.06)
    buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)

    f.wrap_text(screen, screen_size, joke_text, 0.56)
    f.print_tips(screen, screen_size, text)

    # Game Loop
    joke = False
    running = True
    quit_condition = False
    wait = False
    running = True
    lmb_pressed = False
    while running:
        pos = (0, 0)
        hover_changed = False
        hover_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            lmb_pressed = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and not wait and lmb_pressed:
                pos = pygame.mouse.get_pos()
                lmb_pressed = False
            if event.type == pygame.MOUSEMOTION:
                for button in [PlayButton, QuitButton]:
                    if button.update_hover(hover_pos):
                        hover_changed = True
                wait = False

        if hover_changed and not game:
            screen.fill("white")
            f.print_screen(screen, screen_size)
            f.draw_additional_ui_elements(screen, screen_size, joke_text, text)

            for button in [PlayButton, QuitButton]:
                if button.hovered:
                    button.draw_enlarged(screen, buttons_font)
                else:
                    button.draw(screen, buttons_font)

            pygame.display.flip()

        if (pos[0] >= QBPos[0]) and (pos[0] <= QBPos[0] + QBSize[0]) and (pos[1] >= QBPos[1]) and (pos[1] <= QBPos[1] + QBSize[1]) and not game:
            running = False
        if (pos[0] >= PBPos[0]) and (pos[0] <= PBPos[0] + PBSize[0]) and (pos[1] >= PBPos[1]) and (pos[1] <= PBPos[1] + PBSize[1]):
            game = True
            screen.fill("white")
            # Draw the play menu background
            f.draw_play_menu_bg(screen, screen_size)
            Level1Button, Level2Button, Level3Button, BackButton = f.play_menu(
                screen, screen_size, buttons_font)

        if game:
            hover_changed = False
            # Update hover state for each button
            for button in [Level1Button, Level2Button, Level3Button]:
                if button.update_hover(pygame.mouse.get_pos()):
                    hover_changed = True

            if hover_changed:
                screen.fill("white")
                # Draw the play menu background
                f.draw_play_menu_bg(screen, screen_size)
                for button in [Level1Button, Level2Button, Level3Button]:
                    if button.hovered:
                        button.draw_enlarged(screen, buttons_font)
                    else:
                        button.draw(screen, buttons_font)

                pygame.display.flip()

            L1BSize = Level1Button.size
            L1BPos = Level1Button.position
            L2BSize = Level2Button.size
            L2BPos = Level2Button.position
            L3BSize = Level3Button.size
            L3BPos = Level3Button.position
            BBPos = BackButton.position
            BBSize = BackButton.size

            if (pos[0] >= L1BPos[0]) and (pos[0] <= L1BPos[0] + L1BSize[0]) and (pos[1] >= L1BPos[1]) and (pos[1] <= L1BPos[1] + L1BSize[1]):
                quit_condition = f.level_1(screen, screen_size)
                wait = True
            if (pos[0] >= L2BPos[0]) and (pos[0] <= L2BPos[0] + L2BSize[0]) and (pos[1] >= L2BPos[1]) and (pos[1] <= L2BPos[1] + L2BSize[1]):
                quit_condition = f.level_2(screen, screen_size)
                wait = True
            if (pos[0] >= L3BPos[0]) and (pos[0] <= L3BPos[0] + L3BSize[0]) and (pos[1] >= L3BPos[1]) and (pos[1] <= L3BPos[1] + L3BSize[1]):
                quit_condition = f.level_3(screen, screen_size)
                wait = True
            if (pos[0] >= BBPos[0]) and (pos[0] <= BBPos[0] + BBSize[0]) and (pos[1] >= BBPos[1]) and (pos[1] <= BBPos[1] + BBSize[1]):
                screen.fill("white")
                f.print_screen(screen, screen_size)
                PlayButton, QuitButton = f.main_menu(
                    screen, screen_size, enlarge)
                joke_text = f.select_joke()
                text = f.select_tip()
                f.draw_additional_ui_elements(
                    screen, screen_size, joke_text, text)
                game = False
            if quit_condition:
                running = False

        # Update the display
        pygame.display.flip()

    # Exit the game
    pygame.quit()
