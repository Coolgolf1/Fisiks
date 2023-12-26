import functions as f
import pygame


# Initialize Pygame
pygame.init()
joke = False
# Set up the display
screen_size = (960, 540)
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
f.print_screen(screen, screen_size)
PlayButton, SettingsButton, QuitButton = f.main_menu(screen, screen_size)
PBSize = PlayButton.size
PBPos = PlayButton.position
SBSize = SettingsButton.size
SBPos = SettingsButton.position
QBSize = QuitButton.size
QBPos = QuitButton.position
# Game Loop
running = True
while running:
    pos = (0, 0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

        # Handle other events like mouse clicks
            
    # Update game state
    # if not joke:
    #     joke_text = f.select_joke()
    # print(joke_text)
    
    # Menu logic
    if (pos[0] >= PBPos[0]) and (pos[0] <= PBPos[0] + PBSize[0]) and (pos[1] >= PBPos[1]) and (pos[1] <= PBPos[1] + PBSize[1]):
        f.play_menu(screen)
    elif (pos[0] >= SBPos[0]) and (pos[0] <= SBPos[0] + SBSize[0]) and (pos[1] >= SBPos[1]) and (pos[1] <= SBPos[1] + SBSize[1]):
        f.settings_menu(screen)
    elif (pos[0] >= QBPos[0]) and (pos[0] <= QBPos[0] + QBSize[0]) and (pos[1] >= QBPos[1]) and (pos[1] <= QBPos[1] + QBSize[1]):
        running = False

    # Update the display
    pygame.display.flip()

# Exit the game
pygame.quit()
