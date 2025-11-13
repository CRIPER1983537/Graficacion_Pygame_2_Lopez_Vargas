import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Animado")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class AnimatedSprite:
    def __init__(self):
        # Crear una hoja de sprites simple (4 frames)
        self.sprite_sheet = pygame.Surface((400, 100), pygame.SRCALPHA)
        
        # Crear 4 frames de animación (puedes reemplazar con tu hoja de sprites)
        colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0)]
        
        for i in range(4):
            frame_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            
            # Dibujar un personaje simple que cambia en cada frame
            pygame.draw.circle(frame_surface, colors[i], (50, 50), 40)  # Cuerpo
            
            # Brazos que se mueven
            arm_y = 30 + (i * 10)
            pygame.draw.rect(frame_surface, colors[i], (20, arm_y, 60, 10))  # Brazos
            
            # Piernas
            leg_y = 80
            leg_offset = (i - 1.5) * 5
            pygame.draw.rect(frame_surface, colors[i], (35, leg_y, 10, 20))  # Pierna izq
            pygame.draw.rect(frame_surface, colors[i], (55, leg_y, 10, 20))  # Pierna der
            
            # Ojos
            eye_y = 40
            pygame.draw.circle(frame_surface, BLACK, (40, eye_y), 5)  # Ojo izq
            pygame.draw.circle(frame_surface, BLACK, (60, eye_y), 5)  # Ojo der
            
            self.sprite_sheet.blit(frame_surface, (i * 100, 0))
        
        # Configuración de animación
        self.frames = []
        self.frame_width = 100
        self.frame_height = 100
        self.current_frame = 0
        self.animation_speed = 100  # ms entre frames
        self.last_update = pygame.time.get_ticks()
        
        # Extraer frames individuales
        for i in range(4):
            frame = self.sprite_sheet.subsurface(
                (i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            self.frames.append(frame)
    
    def update(self):
        # Cambiar frame según el tiempo
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = current_time
    
    def draw(self, surface, x, y):
        current_image = self.frames[self.current_frame]
        surface.blit(current_image, (x, y))
        
        # Dibujar rectángulo alrededor del frame actual
        pygame.draw.rect(surface, BLACK, (x, y, self.frame_width, self.frame_height), 1)

# Crear sprite animado
sprite = AnimatedSprite()

# Posición del sprite
sprite_x = WIDTH // 2 - 50
sprite_y = HEIGHT // 2 - 50

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
            if event.key == pygame.K_LEFT:
                sprite_x -= 10
            elif event.key == pygame.K_RIGHT:
                sprite_x += 10
            elif event.key == pygame.K_UP:
                sprite_y -= 10
            elif event.key == pygame.K_DOWN:
                sprite_y += 10
    
    # Actualizar animación
    sprite.update()
    
    # Dibujar
    screen.fill(WHITE)
    
    # Dibujar sprite
    sprite.draw(screen, sprite_x, sprite_y)
    
    # Dibujar información
    font = pygame.font.Font(None, 36)
    info_text = font.render("Usa flechas para mover el sprite", True, BLACK)
    frame_text = font.render(f"Frame: {sprite.current_frame + 1}/4", True, BLACK)
    
    screen.blit(info_text, (10, 10))
    screen.blit(frame_text, (10, 50))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()