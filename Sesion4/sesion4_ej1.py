import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rebote con Velocidad Variable")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Parámetros del círculo
circle_radius = 30
circle_x = WIDTH // 2
circle_y = HEIGHT // 2
velocity_x = 5
velocity_y = 3

# Crear reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Actualizar posición
    circle_x += velocity_x
    circle_y += velocity_y
    
    # Rebote en los bordes con aceleración
    if circle_x - circle_radius <= 0 or circle_x + circle_radius >= WIDTH:
        velocity_x = -velocity_x * 1.1  # Aumentar velocidad en 10%
    
    if circle_y - circle_radius <= 0 or circle_y + circle_radius >= HEIGHT:
        velocity_y = -velocity_y * 1.1  # Aumentar velocidad en 10%
    
    # Limitar velocidad máxima
    if abs(velocity_x) > 20:
        velocity_x = 20 if velocity_x > 0 else -20
    if abs(velocity_y) > 20:
        velocity_y = 20 if velocity_y > 0 else -20
    
    # Dibujar
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (int(circle_x), int(circle_y)), circle_radius)
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()