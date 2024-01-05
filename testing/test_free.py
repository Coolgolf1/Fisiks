import pygame
import pymunk

class Lines:
    def __init__(self, points: list):
        self.points = points

space = pymunk.Space()

lines = []
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

screen.fill("white")
pygame.draw.circle(screen, "red", (640, 360), 40)
running = True
cancel = False
drawing = False
points = []
permanent_surface = pygame.Surface(screen.get_size())
permanent_surface.fill("white")
pygame.draw.circle(permanent_surface, "red", (640, 360), 40)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            points = [event.pos]
            cancel = False
            drawing = True
        if event.type == pygame.MOUSEBUTTONUP and not cancel:
            if len(points) > 1:
                pygame.draw.lines(permanent_surface, "blue", False, points, 3) 
            lines.append(Lines(points))
            points = []
            drawing = False
        if event.type == pygame.KEYDOWN and drawing:
            if pygame.K_SPACE:
                points = []  
                cancel = True
                drawing = False  
    
    if pygame.mouse.get_pressed()[0] and not cancel:
        points.append(pygame.mouse.get_pos())
    screen.blit(permanent_surface, (0, 0))
    if len(points) > 1 and not cancel:
        pygame.draw.lines(screen, "gray", False, points, 3)   

    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
