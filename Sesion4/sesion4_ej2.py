import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animación de Pulsación")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Parámetros del círculo
circle_radius = 20
min_radius = 20
max_radius = 50
growing = True
growth_speed = 0.5

# Posición del círculo
circle_x = WIDTH // 2
circle_y = HEIGHT // 2

# Crear reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Actualizar radio (pulsación)
    if growing:
        circle_radius += growth_speed
        if circle_radius >= max_radius:
            growing = False
    else:
        circle_radius -= growth_speed
        if circle_radius <= min_radius:
            growing = True
    
    # Dibujar
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (circle_x, circle_y), int(circle_radius))
    
    # Mostrar información del radio
    font = pygame.font.Font(None, 36)
    radius_text = font.render(f"Radio: {circle_radius:.1f}", True, (0, 0, 0))
    screen.blit(radius_text, (10, 10))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()