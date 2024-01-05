import pygame
import pymunk

class FreehandDrawing:
    def __init__(self, space, points: list, thickness = 5):
        if len(points) < 2:
            return

        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = points[0]
        space.add(self.body)

        self.shapes = []

        for i in range(len(points) - 1):
            start = pymunk.Vec2d(points[i][0], points[i][1]) - pymunk.Vec2d(self.body.position.x, self.body.position.y)
            end = pymunk.Vec2d(points[i + 1][0], points[i + 1][1]) - pymunk.Vec2d(self.body.position.x, self.body.position.y)
            segment_shape = pymunk.Segment(self.body, start, end, thickness)
            segment_shape.elasticity = 0.1
            space.add(segment_shape)
            self.shapes.append(segment_shape)


class StaticLine:
        def __init__(self, space, points, thickness=10):
            self.body = pymunk.Body(0, 0, pymunk.Body.STATIC)
            self.line_shape = pymunk.Segment(self.body, points[0], points[1], thickness)
            self.line_shape.elasticity = 0.5
            space.add(self.body, self.line_shape)

        def draw(self, screen):
            start_pos = self.line_shape.a
            end_pos = self.line_shape.b
            pygame.draw.line(screen, "black", start_pos, end_pos, 5)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
FPS = 144

space = pymunk.Space()
space.gravity = (0, 200)

permanent_surface = pygame.Surface(screen.get_size())
permanent_surface.fill("white")

drawings = []
points = []
drawing = False

static_line = StaticLine(space, [(100, 300), (700, 300)], 5)

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

    static_line.draw(screen)

    if drawing and len(points) > 1:
        pygame.draw.lines(screen, "gray", False, points, 5) 
        
    
    for drawing in drawings:
        for shape in drawing.shapes:
            start_pos = (int(shape.body.position.x + shape.a.x), int(shape.body.position.y + shape.a.y))
            end_pos = (int(shape.body.position.x + shape.b.x), int(shape.body.position.y + shape.b.y))
            pygame.draw.line(screen, "blue", start_pos, end_pos, 5)

    pygame.display.flip()
    clock.tick(FPS)
    space.step(1/FPS)

pygame.quit()
