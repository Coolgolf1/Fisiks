import pygame
import pygame.gfxdraw

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

screen.fill("white")
pygame.draw.circle(screen, "red", (640, 360), 40)
drawing = False
start_pos = None
current_pos = None
running = True
finished = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
            current_pos = event.pos
            drawing = True
            finished = False
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            finished = True
        if event.type == pygame.MOUSEMOTION and drawing:
            current_pos = event.pos

    if drawing:
        screen.fill("white")
        pygame.draw.circle(screen, "red", (640, 360), 40)
        pygame.draw.line(screen, "gray", start_pos, current_pos, 4)
    if finished:
        pygame.draw.line(screen, "blue", start_pos, current_pos, 4)        
        

    pygame.display.flip()

pygame.quit()
