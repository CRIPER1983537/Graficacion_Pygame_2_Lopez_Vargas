import pygame
import sys
import math
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nave Espacial - Rotación y Movimiento")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

class Spaceship:
    def __init__(self, image_path="NAVE"):
        # Intentar diferentes extensiones de archivo
        extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        image_loaded = False
        
        for ext in extensions:
            full_path = image_path + ext
            try:
                if os.path.exists(full_path):
                    self.original_image = pygame.image.load(full_path).convert_alpha()
                    print(f"Imagen cargada exitosamente: {full_path}")
                    print(f"Tamaño original: {self.original_image.get_size()}")
                    image_loaded = True
                    
                    # Escalar a tamaño adecuado si es muy grande o muy pequeña
                    original_width, original_height = self.original_image.get_size()
                    if original_width > 150 or original_height > 150 or original_width < 30:
                        # Redimensionar manteniendo proporciones
                        target_size = 80
                        scale_factor = min(target_size/original_width, target_size/original_height)
                        new_width = int(original_width * scale_factor)
                        new_height = int(original_height * scale_factor)
                        self.original_image = pygame.transform.scale(
                            self.original_image, (new_width, new_height)
                        )
                        print(f"Imagen escalada a: {new_width}x{new_height}")
                    break
                    
            except pygame.error as e:
                print(f"Error cargando {full_path}: {e}")
                continue
        
        # Si no se pudo cargar ninguna imagen, crear una por defecto
        if not image_loaded:
            print("No se encontró la imagen NAVE. Creando nave por defecto...")
            self.original_image = self.create_default_ship()
        
        # Propiedades de la nave
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.angle = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.deceleration = 0.05
        
    def create_default_ship(self):
        """Crear una nave por defecto si no se encuentra la imagen"""
        ship_surface = pygame.Surface((80, 60), pygame.SRCALPHA)
        
        # Dibujar nave más detallada
        # Cuerpo principal
        pygame.draw.polygon(ship_surface, (100, 150, 255), [
            (40, 0),    # Punta
            (10, 20),   # Ala izquierda frontal
            (5, 40),    # Ala izquierda trasera  
            (25, 50),   # Cuerpo izquierdo
            (40, 60),   # Cola
            (55, 50),   # Cuerpo derecho
            (75, 40),   # Ala derecha trasera
            (70, 20)    # Ala derecha frontal
        ])
        
        # Ventana de cabina
        pygame.draw.circle(ship_surface, (200, 230, 255), (40, 20), 8)
        
        # Detalles de las alas
        pygame.draw.polygon(ship_surface, (80, 120, 220), [
            (15, 25), (8, 38), (22, 45)
        ])
        pygame.draw.polygon(ship_surface, (80, 120, 220), [
            (65, 25), (72, 38), (58, 45)
        ])
        
        # Propulsores
        pygame.draw.rect(ship_surface, (50, 50, 70), (30, 55, 5, 8))
        pygame.draw.rect(ship_surface, (50, 50, 70), (45, 55, 5, 8))
        
        return ship_surface
        
    def update(self, mouse_pos):
        # Calcular ángulo hacia el ratón
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        target_angle = math.degrees(math.atan2(-dy, dx)) - 90
        
        # Suavizar la rotación
        angle_diff = (target_angle - self.angle) % 360
        if angle_diff > 180:
            angle_diff -= 360
        
        self.angle += angle_diff * 0.1  # Suavizado del 10%
        
        # Rotar imagen
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Mantener el centro después de la rotación
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # Aplicar deceleración
        if self.speed > 0:
            self.speed = max(0, self.speed - self.deceleration)
        
        # Mover según la dirección y velocidad
        if self.speed > 0:
            rad_angle = math.radians(self.angle + 90)  # Ajustar por la rotación inicial
            self.rect.x += math.cos(rad_angle) * self.speed
            self.rect.y -= math.sin(rad_angle) * self.speed
            
            # Mantener dentro de la pantalla (envolver)
            if self.rect.right < 0:
                self.rect.left = WIDTH
            elif self.rect.left > WIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = HEIGHT
            elif self.rect.top > HEIGHT:
                self.rect.bottom = 0
    
    def accelerate(self):
        self.speed = min(self.speed + self.acceleration, self.max_speed)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
        # Dibujar línea hacia el ratón (opcional)
        pygame.draw.line(surface, RED, self.rect.center, pygame.mouse.get_pos(), 2)
        
        # Dibujar estela si se está moviendo
        if self.speed > 0:
            trail_length = int(self.speed * 10)
            rad_angle = math.radians(self.angle + 90)
            start_x = self.rect.centerx - math.cos(rad_angle) * 30
            start_y = self.rect.centery + math.sin(rad_angle) * 30
            
            for i in range(3):
                trail_x = start_x - math.cos(rad_angle) * (trail_length * (i + 1) / 3)
                trail_y = start_y + math.sin(rad_angle) * (trail_length * (i + 1) / 3)
                size = max(1, 3 - i)
                color_val = max(100, 255 - i * 80)
                pygame.draw.circle(surface, (color_val, color_val, 255), 
                                 (int(trail_x), int(trail_y)), size)

# Crear nave - busca la imagen "NAVE" con diferentes extensiones
spaceship = Spaceship("NAVE")

# Crear reloj
clock = pygame.time.Clock()

# Bucle principal
running = True
moving_forward = False

while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                moving_forward = True
            elif event.key == pygame.K_SPACE:
                # Turbo
                spaceship.speed = spaceship.max_speed
            elif event.key == pygame.K_r:
                # Reiniciar posición
                spaceship.rect.center = (WIDTH//2, HEIGHT//2)
                spaceship.speed = 0
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                moving_forward = False
    
    # Obtener posición del ratón
    mouse_pos = pygame.mouse.get_pos()
    
    # Actualizar nave
    spaceship.update(mouse_pos)
    
    # Acelerar si se presiona la tecla
    if moving_forward:
        spaceship.accelerate()
    
    # Dibujar
    screen.fill(BLACK)
    
    # Dibujar estrellas de fondo animadas
    current_time = pygame.time.get_ticks()
    for i in range(100):
        x = (i * 157) % WIDTH
        y = (i * 233) % HEIGHT
        size = (i % 3) + 1
        brightness = 150 + int(50 * math.sin(current_time * 0.001 + i))
        color = (brightness, brightness, brightness)
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Dibujar nave
    spaceship.draw(screen)
    
    # Dibujar información
    font = pygame.font.Font(None, 32)
    controls = [
        "CONTROLES:",
        "Mover ratón: Rotar nave",
        "FLECHA ARRIBA / W: Avanzar", 
        "ESPACIO: Turbo instantáneo",
        "R: Reiniciar posición",
        "ESC: Salir"
    ]
    
    for i, text in enumerate(controls):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10 + i * 35))
    
    # Información de estado
    status_font = pygame.font.Font(None, 28)
    speed_text = status_font.render(f"Velocidad: {spaceship.speed:.1f}", True, (100, 255, 100))
    angle_text = status_font.render(f"Ángulo: {spaceship.angle:.1f}°", True, (100, 255, 100))
    pos_text = status_font.render(f"Posición: ({spaceship.rect.centerx}, {spaceship.rect.centery})", 
                                True, (100, 255, 100))
    
    screen.blit(speed_text, (WIDTH - 200, 20))
    screen.blit(angle_text, (WIDTH - 200, 50))
    screen.blit(pos_text, (WIDTH - 200, 80))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()