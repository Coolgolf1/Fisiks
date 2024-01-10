import pygame
import pymunk


class Button:
    def __init__(self, position: tuple, size: tuple, outline_width: int, text: str, colour: str):
        self.colour = colour
        self.position = position
        self.size = size
        self.outline_width = outline_width
        self.text = text
        self.original_size = size
        self.hovered = False

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.colour, [
                         self.position[0], self.position[1], self.size[0], self.size[1]], self.outline_width)

        text_surface = font.render(self.text, True, self.colour)

        text_rect = text_surface.get_rect(center=(
            self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2))

        screen.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        # Check if the mouse is over the button
        if (self.position[0] <= mouse_pos[0] <= self.position[0] + self.size[0] and
                self.position[1] <= mouse_pos[1] <= self.position[1] + self.size[1]):
            if not self.hovered:  # Only change state if it was previously not hovered
                self.hovered = True
                return True
        else:
            self.hovered = False
        return False

    def draw_enlarged(self, screen, font):
        # Calculate the enlarged size
        enlargement_factor = 1.1
        enlarged_size = (
            int(self.size[0] * enlargement_factor), int(self.size[1] * enlargement_factor))
        # Center the enlarged button on the original position
        enlarged_position = (self.position[0] - (enlarged_size[0] - self.size[0]) // 2,
                             self.position[1] - (enlarged_size[1] - self.size[1]) // 2)

        # Drawing the enlarged button
        pygame.draw.rect(screen, [255, 255, 255], [
                         *enlarged_position, *enlarged_size])
        pygame.draw.rect(screen, self.colour, [
                         *enlarged_position, *enlarged_size], self.outline_width)

        text_surface = font.render(self.text, True, self.colour)
        text_rect = text_surface.get_rect(center=(enlarged_position[0] + enlarged_size[0] // 2,
                                                  enlarged_position[1] + enlarged_size[1] // 2))
        screen.blit(text_surface, text_rect)

    def update_hover(self, mouse_pos):
        """ Update the hover state and return True if the state changed. """
        previously_hovered = self.hovered
        self.hovered = self.position[0] <= mouse_pos[0] <= self.position[0] + self.size[0] and \
            self.position[1] <= mouse_pos[1] <= self.position[1] + self.size[1]
        return self.hovered != previously_hovered


class FreehandDrawing:
    def __init__(self, space, points: list, thickness=10):
        if len(points) < 2:
            return

        centroid = pymunk.Vec2d(*points[0])
        for point in points[1:]:
            centroid += pymunk.Vec2d(*point)
        centroid /= len(points)

        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = centroid
        space.add(self.body)

        self.shapes = []

        for i in range(len(points) - 1):
            start = pymunk.Vec2d(*points[i]) - self.body.position
            end = pymunk.Vec2d(*points[i + 1]) - self.body.position
            segment_shape = pymunk.Segment(self.body, start, end, thickness//2)
            segment_shape.elasticity = 0.3
            segment_shape.friction = 0.6
            space.add(segment_shape)
            self.shapes.append(segment_shape)


class StaticLine:
    def __init__(self, space, points, thickness):
        self.thickness = thickness
        self.body = pymunk.Body(0, 0, pymunk.Body.STATIC)
        self.line_shape = pymunk.Segment(
            self.body, points[0], points[1], self.thickness//2)
        self.line_shape.elasticity = 0.6
        self.line_shape.friction = 0.8
        self.collision_type = 2
        space.add(self.body, self.line_shape)

    def draw(self, screen):
        start_pos = self.line_shape.a
        end_pos = self.line_shape.b
        pygame.draw.line(screen, "black", start_pos, end_pos, self.thickness)

    def jar_draw(self, screen):
        self.line_shape.elasticity = 0
        self.line_shape.friction = 2
        start_pos = self.line_shape.a
        end_pos = self.line_shape.b
        pygame.draw.line(screen, "green", start_pos, end_pos, self.thickness)

    def spring_draw_floor(self, screen):
        self.line_shape.elasticity = 1.8
        start_pos = self.line_shape.a
        end_pos = self.line_shape.b
        pygame.draw.line(screen, "orange", start_pos, end_pos, self.thickness)

    def spring_draw_wall(self, screen):
        self.line_shape.elasticity = 7
        start_pos = self.line_shape.a
        end_pos = self.line_shape.b
        pygame.draw.line(screen, "red", start_pos, end_pos, self.thickness)


class Ball:
    def __init__(self, space, pos, radius):
        self.radius = radius
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, self.radius, (0, 0))
        self.body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 1
        self.shape.friction = 0.2
        self.collision_type = 1
        space.add(self.body, self.shape)

    def draw(self, screen):
        pos = int(self.body.position.x), int(self.body.position.y)
        angle = self.body.angle
        pygame.draw.circle(screen, [231, 84, 128], pos, self.radius)
        end_line = pymunk.Vec2d(self.radius, 0).rotated(angle)
        pygame.draw.line(screen, "blue", pos,
                         (pos[0] + end_line.x, pos[1] + end_line.y), 2)
        pygame.draw.line(screen, "blue", pos,
                         (pos[0] - end_line.x, pos[1] - end_line.y), 2)

