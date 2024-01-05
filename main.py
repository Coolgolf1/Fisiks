import functions as f
import pygame


game = False
settings = False

pygame.init()

screen_size = (1280, 720)
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))

f.print_screen(screen, screen_size)

joke_text = f.select_joke(screen_size)


PlayButton, SettingsButton, QuitButton = f.main_menu(
    screen, screen_size, joke_text)
PBSize = PlayButton.size
PBPos = PlayButton.position
SBSize = SettingsButton.size
SBPos = SettingsButton.position
QBSize = QuitButton.size
QBPos = QuitButton.position

# Game Loop
joke = False
running = True
quit_condition = False
while running:
    pos = (0, 0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

    # Update game state
    # Menu logic
    if (pos[0] >= PBPos[0]) and (pos[0] <= PBPos[0] + PBSize[0]) and (pos[1] >= PBPos[1]) and (pos[1] <= PBPos[1] + PBSize[1]):
        game = True
        Level1Button, Level2Button, Level3Button = f.play_menu(
            screen, screen_size)
        L1BSize = Level1Button.size
        L1BPos = Level1Button.position
        L2BSize = Level2Button.size
        L2BPos = Level2Button.position
        L3BSize = Level3Button.size
        L3BPos = Level3Button.position

    elif (pos[0] >= SBPos[0]) and (pos[0] <= SBPos[0] + SBSize[0]) and (pos[1] >= SBPos[1]) and (pos[1] <= SBPos[1] + SBSize[1]):
        settings = True
        f.settings_menu(screen, screen_size)
    elif (pos[0] >= QBPos[0]) and (pos[0] <= QBPos[0] + QBSize[0]) and (pos[1] >= QBPos[1]) and (pos[1] <= QBPos[1] + QBSize[1]):
        running = False
    if game:
        if (pos[0] >= L1BPos[0]) and (pos[0] <= L1BPos[0] + L1BSize[0]) and (pos[1] >= L1BPos[1]) and (pos[1] <= L1BPos[1] + L1BSize[1]):
            quit_condition = f.level_1(screen, screen_size)
        if (pos[0] >= L2BPos[0]) and (pos[0] <= L2BPos[0] + L2BSize[0]) and (pos[1] >= L2BPos[1]) and (pos[1] <= L2BPos[1] + L2BSize[1]):
            quit_condition = f.level_2(screen, screen_size)
        if (pos[0] >= L3BPos[0]) and (pos[0] <= L3BPos[0] + L3BSize[0]) and (pos[1] >= L3BPos[1]) and (pos[1] <= L3BPos[1] + L3BSize[1]):
            quit_condition = f.level_3(screen, screen_size)
        if quit_condition: 
            running = False
    if settings:
        pass

    # Update the display
    pygame.display.flip()

# Exit the game
pygame.quit()
