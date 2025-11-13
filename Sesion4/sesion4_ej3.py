import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Gravedad")

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Parámetros del círculo
circle_radius = 30
circle_x = WIDTH // 2
circle_y = 100  # Comienza desde arriba

# Parámetros de física
velocity_y = 0
gravity = 0.5
energy_loss = 0.8  # Pérdida del 20% de energía en cada rebote
floor_y = HEIGHT - circle_radius

# Crear reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Reiniciar simulación al presionar espacio
                circle_y = 100
                velocity_y = 0
    
    # Aplicar gravedad
    velocity_y += gravity
    
    # Actualizar posición
    circle_y += velocity_y
    
    # Rebote en el suelo con pérdida de energía
    if circle_y >= floor_y:
        circle_y = floor_y
        velocity_y = -velocity_y * energy_loss  # Rebote con pérdida de energía
        
        # Detener la animación si la velocidad es muy pequeña
        if abs(velocity_y) < 0.5:
            velocity_y = 0
    
    # Dibujar
    screen.fill(WHITE)
    
    # Dibujar suelo
    pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT), (WIDTH, HEIGHT), 2)
    
    # Dibujar círculo
    pygame.draw.circle(screen, GREEN, (int(circle_x), int(circle_y)), circle_radius)
    
    # Mostrar información
    font = pygame.font.Font(None, 36)
    velocity_text = font.render(f"Velocidad Y: {velocity_y:.2f}", True, (0, 0, 0))
    height_text = font.render(f"Altura: {HEIGHT - circle_y:.1f}", True, (0, 0, 0))
    info_text = font.render("Presiona ESPACIO para reiniciar", True, (0, 0, 0))
    
    screen.blit(velocity_text, (10, 10))
    screen.blit(height_text, (10, 50))
    screen.blit(info_text, (10, HEIGHT - 40))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()