import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colisión con Cambio de Color")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Jugador
player_width, player_height = 50, 50
player_x = 100
player_y = HEIGHT // 2 - player_height // 2
player_color = BLUE
player_speed = 5

# Objetivo
target_width, target_height = 70, 70
target_x = 600
target_y = HEIGHT // 2 - target_height // 2
target_color = RED

# Crear reloj
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Obtener teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Mover jugador
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
        player_y += player_speed
    
    # Crear rectángulos para detección de colisión
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    target_rect = pygame.Rect(target_x, target_y, target_width, target_height)
    
    # Detectar colisión y cambiar color
    if player_rect.colliderect(target_rect):
        player_color = GREEN  # Cambiar a verde cuando colisiona
    else:
        player_color = BLUE   # Volver a azul cuando no colisiona
    
    # Dibujar
    screen.fill(WHITE)
    
    # Dibujar objetivo
    pygame.draw.rect(screen, target_color, (target_x, target_y, target_width, target_height))
    
    # Dibujar jugador
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))
    
    # Mostrar información
    font = pygame.font.Font(None, 36)
    info_text = font.render("Usa las flechas para mover el cuadrado azul", True, (0, 0, 0))
    collision_text = font.render("COLISIÓN DETECTADA" if player_color == GREEN else "Sin colisión", True, (0, 0, 0))
    
    screen.blit(info_text, (10, 10))
    screen.blit(collision_text, (10, 50))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()