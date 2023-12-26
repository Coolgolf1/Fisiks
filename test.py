import pygame
import pygame.gfxdraw

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

    screen.fill("white")
    pygame.draw.circle(screen, "red", (640, 360), 40)
    pygame.gfxdraw.line(screen, 40, 80, 90, 102, (0, 0, 0))


    pygame.display.flip()

pygame.quit()
