import functions as f
import pygame

pygame.init()
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Fisiks - Test.py")
bg = pygame.image.load(".\\assets\\test_bg.png")
bg = pygame.transform.scale(bg, (screen_size[0], screen_size[1]))
screen.blit(bg, (0, 0))

# Si se imprimen los dos botones de jugar y salir a la izquierda y un rectángulo a la derecha, funciona.
f.main_menu(screen, screen_size, False)

# Si se imprime el texto de prueba en la caja derecha, funciona.
f.wrap_text(screen, screen_size,
            "¡Hola, esto es una prueba para el test.py!", 0.3)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()
