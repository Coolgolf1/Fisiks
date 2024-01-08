import functions as f
import pygame

game = False
settings = False

pygame.init()
screen_size = (1280, 720)
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
screen.fill("white")
ChangeResolutionButton, Res1Button, Res2Button, Res3Button, Res4Button = f.choose_resolution(screen, screen_size)
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

running = True
while running:
    pos = (0, 0)
    hover_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos() 

    if (pos[0] >= R1BPos[0]) and (pos[0] <= R1BPos[0] + R1BSize[0]) and (pos[1] >= R1BPos[1]) and (pos[1] <= R1BPos[1] + R1BSize[1]):
        screen_size = (1920, 1080)
    elif (pos[0] >= R2BPos[0]) and (pos[0] <= R2BPos[0] + R2BSize[0]) and (pos[1] >= R2BPos[1]) and (pos[1] <= R2BPos[1] + R2BSize[1]):
        screen_size = (1280, 720)
    elif (pos[0] >= R3BPos[0]) and (pos[0] <= R3BPos[0] + R3BSize[0]) and (pos[1] >= R3BPos[1]) and (pos[1] <= R3BPos[1] + R3BSize[1]):
        screen_size = (1920, 1200)
    elif (pos[0] >= R4BPos[0]) and (pos[0] <= R4BPos[0] + R4BSize[0]) and (pos[1] >= R4BPos[1]) and (pos[1] <= R4BPos[1] + R4BSize[1]):
        screen_size = (1280, 800)
    elif (pos[0] >= CRBPos[0]) and (pos[0] <= CRBPos[0] + CRBSize[0]) and (pos[1] >= CRBPos[1]) and (pos[1] <= CRBPos[1] + CRBSize[1]):
        screen = pygame.display.set_mode(screen_size)
        running = False
    
    pygame.display.flip()

pygame.quit()

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('.\\assets\\music.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)

screen = pygame.display.set_mode((screen_size[0], screen_size[1]))


buttons_font_size = int(screen_size[1] * 0.06)
buttons_font = pygame.font.SysFont("Calibri", buttons_font_size)

f.print_screen(screen, screen_size)

joke_text = f.select_joke(screen_size)

enlarge = False
PlayButton, QuitButton = f.main_menu(
    screen, screen_size, joke_text, enlarge)
PBSize = PlayButton.size
PBPos = PlayButton.position
QBSize = QuitButton.size
QBPos = QuitButton.position
enlarged_font_size = int(screen_size[1] * 0.07)
enlarged_font = pygame.font.SysFont("Calibri", enlarged_font_size)

# Game Loop
joke = False
running = True
quit_condition = False
wait = False
running = True
while running:
    pos = (0, 0)
    hover_changed = False
    hover_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and not wait:
            pos = pygame.mouse.get_pos() 
        if event.type == pygame.MOUSEMOTION:
            for button in [PlayButton, QuitButton]:
                if button.update_hover(hover_pos):
                    hover_changed = True
            wait = False 

    if hover_changed and not game and not settings:
        screen.fill("white")
        f.print_screen(screen, screen_size)
        f.draw_additional_ui_elements(screen, screen_size, joke_text)

        for button in [PlayButton, QuitButton]:
            if button.hovered:
                button.draw_enlarged(screen, buttons_font)
            else:
                button.draw(screen, buttons_font)

        pygame.display.flip()


    # if (pos[0] >= SBPos[0]) and (pos[0] <= SBPos[0] + SBSize[0]) and (pos[1] >= SBPos[1]) and (pos[1] <= SBPos[1] + SBSize[1]) and not game and not settings:
    #     settings = True
    if (pos[0] >= QBPos[0]) and (pos[0] <= QBPos[0] + QBSize[0]) and (pos[1] >= QBPos[1]) and (pos[1] <= QBPos[1] + QBSize[1]) and not game and not settings:
        running = False
    if (pos[0] >= PBPos[0]) and (pos[0] <= PBPos[0] + PBSize[0]) and (pos[1] >= PBPos[1]) and (pos[1] <= PBPos[1] + PBSize[1]):
        game = True
        Level1Button, Level2Button, Level3Button, BackButton = f.play_menu(
            screen, screen_size)
        L1BSize = Level1Button.size
        L1BPos = Level1Button.position
        L2BSize = Level2Button.size
        L2BPos = Level2Button.position
        L3BSize = Level3Button.size
        L3BPos = Level3Button.position
        BBPos = BackButton.position
        BBSize = BackButton.size
    if game:
        if (pos[0] >= L1BPos[0]) and (pos[0] <= L1BPos[0] + L1BSize[0]) and (pos[1] >= L1BPos[1]) and (pos[1] <= L1BPos[1] + L1BSize[1]):
            quit_condition = f.level_1(screen, screen_size)
        if (pos[0] >= L2BPos[0]) and (pos[0] <= L2BPos[0] + L2BSize[0]) and (pos[1] >= L2BPos[1]) and (pos[1] <= L2BPos[1] + L2BSize[1]):
            quit_condition = f.level_2(screen, screen_size)
        if (pos[0] >= L3BPos[0]) and (pos[0] <= L3BPos[0] + L3BSize[0]) and (pos[1] >= L3BPos[1]) and (pos[1] <= L3BPos[1] + L3BSize[1]):
            quit_condition = f.level_3(screen, screen_size)
            wait = True
        if (pos[0] >= BBPos[0]) and (pos[0] <= BBPos[0] + BBSize[0]) and (pos[1] >= BBPos[1]) and (pos[1] <= BBPos[1] + BBSize[1]):
            screen.fill("white")
            f.print_screen(screen, screen_size)
            PlayButton, QuitButton = f.main_menu(
                screen, screen_size, joke_text, enlarge)
            game = False
        if quit_condition:
            running = False
    # if settings:
    #     quit_condition = f.settings(screen, screen_size)
    #     if quit_condition:
    #         running = False
    #     settings = False
        
    # Update the display
    pygame.display.flip()

# Exit the game
pygame.quit()
