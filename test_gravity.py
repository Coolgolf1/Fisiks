import pygame
import pymunk


# def NewBall(space, pos):
#     body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
#     body.position = pos
#     shape = pymunk.Circle(body, 10)
#     shape.elasticity = 0.8
#     space.add(body, shape)
#     return shape

def NewLine(space, pos):
    start = (pos[0], pos[1])
    end = (pos[0] + 10, pos[1]) 
    moment = pymunk.moment_for_segment(1, start, end, 10)
    line_body = pymunk.Body(1, moment, body_type=pymunk.Body.DYNAMIC)
    line_body.position = pos
    line_body_shape = pymunk.Segment(line_body, (0, 0), (10, 20), 10) 
    line_body_shape.elasticity = 0.1
    space.add(line_body, line_body_shape)
    return line_body_shape

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
FPS = 60

space = pymunk.Space()
space.gravity = (0, 200)

static_ball_body = pymunk.Body(body_type=pymunk.Body.STATIC)
static_ball_body.position = (300, 300)
static_ball_shape = pymunk.Circle(static_ball_body, 30)
static_ball_shape.elasticity = 0.9
space.add(static_ball_body, static_ball_shape)

segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_body_line = pymunk.Segment(segment_body, (0, 350), (600, 400), 5)
segment_body_line.elasticity = 1
space.add(segment_body, segment_body_line)

drawing_line = False
start_line_pos = None

lines = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            lines.append(NewLine(space, event.pos))


    screen.fill("white")

    for line in lines:
        start_pos = line.a + line.body.position
        end_pos = line.b + line.body.position
        pygame.draw.line(screen, "black", start_pos, end_pos, 10)
    pygame.draw.circle(screen, "red", static_ball_body.position, 30)
    pygame.draw.line(screen, "red", (0, 350), (600, 400), 3)

    pygame.display.flip()
    clock.tick(FPS)
    space.step(1/FPS)


pygame.quit()