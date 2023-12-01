from functions import *

pygame.init()

pygame.display.set_caption("My Pygame Window")
screen()

running = True
while running:
   
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    menu_screen()
    # Update the display
    pygame.display.flip()

pygame.quit()
