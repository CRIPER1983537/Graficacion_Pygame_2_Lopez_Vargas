import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ajuste de Tamaño Dinámico")

# Cargar imagen (usa una imagen de ejemplo o reemplaza con tu ruta)
try:
    # Intentar cargar una imagen (puedes reemplazar con tu propia imagen)
    image_path = "player.png"  # Cambia por tu imagen
    if not os.path.exists(image_path):
        # Crear una superficie temporal si no existe la imagen
        original_image = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.circle(original_image, (255, 0, 0), (50, 50), 50)
        pygame.draw.rect(original_image, (0, 0, 255), (30, 30, 40, 40))
    else:
        original_image = pygame.image.load(image_path).convert_alpha()
except:
    # Surface de respaldo
    original_image = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(original_image, (255, 0, 0), (50, 50), 50)

# Variables de tamaño
scale_factor = 1.0
min_scale = 0.1
max_scale = 3.0
scale_step = 0.1

# Posición central
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Crear reloj
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                scale_factor = min(scale_factor + scale_step, max_scale)
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                scale_factor = max(scale_factor - scale_step, min_scale)
            elif event.key == pygame.K_r:  # Resetear tamaño
                scale_factor = 1.0
    
    # Calcular nuevo tamaño manteniendo proporciones
    original_width, original_height = original_image.get_size()
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    
    # Escalar imagen manteniendo proporciones
    scaled_image = pygame.transform.scale(original_image, (new_width, new_height))
    
    # Calcular posición para mantener centrado
    image_rect = scaled_image.get_rect(center=(center_x, center_y))
    
    # Dibujar
    screen.fill((240, 240, 240))
    
    # Dibujar imagen escalada
    screen.blit(scaled_image, image_rect)
    
    # Dibujar información
    font = pygame.font.Font(None, 36)
    info_text = font.render(f"Tamaño: {scale_factor:.1f}x (+/- para ajustar, R para reset)", True, (0, 0, 0))
    size_text = font.render(f"Dimensiones: {new_width} x {new_height}", True, (0, 0, 0))
    
    screen.blit(info_text, (10, 10))
    screen.blit(size_text, (10, 50))
    
    # Dibujar borde alrededor de la imagen
    pygame.draw.rect(screen, (0, 0, 0), image_rect, 2)
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()