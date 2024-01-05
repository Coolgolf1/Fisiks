import pygame
import pymunk
import pymunk.pygame_util
from classes import *

pygame.init()

screen = pygame.display.set_mode((1280, 720))
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
thickness = 5

lines.append(StaticLine(space, [(400, 175), (1280, 175)], 10))
lines.append(StaticLine(space, [(0, 350), (880, 350)], 10))
lines.append(StaticLine(space, [(400, 525), (1280, 525)], 10))
lines.append(StaticLine(space, [(0, 0), (0, 720)], 1))
lines.append(StaticLine(space, [(1280, 0), (1280, 720)], 1))
# Jar
jar_lines.append(StaticLine(space, [(1230, 720), (1080, 720)], 5))
jar_lines.append(StaticLine(space, [(1230, 720), (1280, 600)], 5))
jar_lines.append(StaticLine(space, [(1080, 720), (1030, 600)], 5))
# Ball
ball = Ball(space, (1200, 100))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            points = [event.pos]
            drawing = True
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and len(points) > 1:
                drawings.append(FreehandDrawing(space, points))
            points = []
            drawing = False
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                points.append(event.pos)

    screen.blit(permanent_surface, (0, 0))

    ball.draw(screen)

    # space.debug_draw(draw_options)

    for line in lines:
        line.draw(screen)
    
    for line in jar_lines:
        line.jar_draw(screen)

    if drawing and len(points) > 1:
        pygame.draw.lines(screen, "gray", False, points, 5)

    for drawing in drawings:
        for shape in drawing.shapes:
            start_world = drawing.body.position + shape.a.rotated(drawing.body.angle)
            end_world = drawing.body.position + shape.b.rotated(drawing.body.angle)
            pygame.draw.line(screen, "blue", start_world, end_world, thickness)

    pygame.display.flip()
    clock.tick(FPS)
    space.step(1/FPS)

pygame.quit()