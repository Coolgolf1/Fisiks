import pygame


class Button:
    def __init__(self, position: tuple, size: tuple, outline_width: int, text: str):
        self.position = position
        self.size = size
        self.outline_width = outline_width
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, [0, 0, 0], [
                         self.position[0], self.position[1], self.size[0], self.size[1]], self.outline_width)

        text_surface = font.render(self.text, True, [0, 0, 0])

        text_rect = text_surface.get_rect(center=(
            self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2))

        screen.blit(text_surface, text_rect)
