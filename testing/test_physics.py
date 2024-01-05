import pygame
import pymunk

class FreehandLine:
    def __init__(self, space, points, thickness=5):
        self.space = space
        self.points = points
        self.thickness = thickness
        self.shapes = []
        self.create_line_segments()

    def create_line_segments(self):
        for i in range(len(self.points) - 1):
            body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
            shape = pymunk.Segment(body, self.points[i], self.points[i + 1], self.thickness)
            shape.friction = 0.5
            self.space.add(body, shape)
            self.shapes.append(shape)

    def draw(self, screen):
        for segment in self.shapes:
            body = segment.body
            pv1 = body.position + segment.a.rotated(body.angle) 
            pv2 = body.position + segment.b.rotated(body.angle)
            pygame.draw.line(screen, (0, 0, 0), pv1, pv2, self.thickness)

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 900)

running = True
drawing = False
current_line = []
lines = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            current_line.append(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            if len(current_line) > 1:
                freehand_line = FreehandLine(space, current_line)
                lines.append(freehand_line)
            current_line.clear()

    if drawing:
        current_line.append(pygame.mouse.get_pos())

    screen.fill("white")
    for line in lines:
        line.draw(screen)

    space.step(1/60)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
