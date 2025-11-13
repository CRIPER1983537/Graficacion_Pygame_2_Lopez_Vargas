import pygame
import sys
import random
import math
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nave Slayer - Recolecta y Evita")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Cargar imagen de la nave
def load_ship_image():
    image_name = "NaveSlayer.png"
    try:
        if os.path.exists(image_name):
            image = pygame.image.load(image_name).convert_alpha()
            print(f"Imagen cargada exitosamente: {image_name}")
            print(f"Tamaño original: {image.get_size()}")
            
            # Escalar a tamaño adecuado manteniendo proporciones
            original_width, original_height = image.get_size()
            target_width = 60  # Ancho objetivo
            scale_factor = target_width / original_width
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            
            image = pygame.transform.scale(image, (new_width, new_height))
            print(f"Imagen escalada a: {new_width}x{new_height}")
            return image
        else:
            print(f"Error: No se encontró la imagen {image_name}")
    except pygame.error as e:
        print(f"Error cargando {image_name}: {e}")
    
    # Si no se encuentra la imagen, crear una por defecto
    print("Creando nave por defecto...")
    image = pygame.Surface((60, 80), pygame.SRCALPHA)
    # Dibujar nave estilo arcade mejorada
    points = [
        (30, 0), (10, 40), (15, 80), (45, 80), (50, 40)
    ]
    pygame.draw.polygon(image, PURPLE, points)
    pygame.draw.polygon(image, WHITE, points, 3)
    # Detalles
    pygame.draw.circle(image, (200, 230, 255), (30, 25), 10)  # Cabina
    pygame.draw.rect(image, RED, (18, 65, 8, 15))  # Propulsor izquierdo
    pygame.draw.rect(image, RED, (34, 65, 8, 15))  # Propulsor derecho
    # Alas
    pygame.draw.polygon(image, BLUE, [(5, 45), (0, 60), (15, 60)])
    pygame.draw.polygon(image, BLUE, [(55, 45), (60, 60), (45, 60)])
    return image

# Clase de la Nave
class Spaceship:
    def __init__(self):
        self.image = load_ship_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 50
        self.speed = 6
        self.mask = pygame.mask.from_surface(self.image)  # Para colisiones precisas
        self.thrust_timer = 0
    
    def move(self, keys):
        moving = False
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            moving = True
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            moving = True
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            moving = True
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            moving = True
        
        return moving
    
    def draw(self, moving):
        screen.blit(self.image, self.rect)
        
        # Dibujar efecto de propulsión cuando se mueve
        if moving:
            self.thrust_timer += 1
            prop_x = self.rect.centerx
            prop_y = self.rect.bottom
            
            # Efecto de llamas animadas
            for i in range(3):
                flame_length = random.randint(15, 25)
                flame_width = random.randint(4, 8)
                
                # Colores de llama que cambian
                if self.thrust_timer % 10 < 5:
                    flame_color = (255, random.randint(150, 255), 0)  # Naranja-amarillo
                else:
                    flame_color = (255, 0, 0)  # Rojo
                
                # Forma de llama irregular
                points = [
                    (prop_x - flame_width//2, prop_y),
                    (prop_x - flame_width, prop_y + flame_length),
                    (prop_x + flame_width, prop_y + flame_length),
                    (prop_x + flame_width//2, prop_y)
                ]
                pygame.draw.polygon(screen, flame_color, points)
                
                # Núcleo de la llama
                core_length = flame_length - 5
                pygame.draw.polygon(screen, YELLOW, [
                    (prop_x - 2, prop_y),
                    (prop_x - 3, prop_y + core_length),
                    (prop_x + 3, prop_y + core_length),
                    (prop_x + 2, prop_y)
                ])

# Clase de los Puntos (para recolectar)
class Point:
    def __init__(self):
        self.radius = 12
        self.respawn()
        self.color = GREEN
        self.glow_timer = 0
        self.collected = False
    
    def respawn(self):
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(-100, -self.radius)
        self.speed = random.uniform(1.0, 2.5)
        self.collected = False
    
    def update(self):
        self.y += self.speed
        self.glow_timer += 1
        if self.y > HEIGHT + self.radius:
            self.respawn()
    
    def draw(self):
        if self.collected:
            return
            
        # Efecto de brillo pulsante
        glow = abs(math.sin(self.glow_timer * 0.1)) * 50 + 150
        current_color = (0, min(255, int(glow)), 0)
        
        pygame.draw.circle(screen, current_color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius, 2)
        
        # Efecto de destello rotatorio
        for i in range(4):
            angle = self.glow_timer * 0.2 + i * math.pi / 2
            spark_x = self.x + math.cos(angle) * (self.radius + 8)
            spark_y = self.y + math.sin(angle) * (self.radius + 8)
            spark_size = 2 + math.sin(angle) * 1
            pygame.draw.circle(screen, YELLOW, (int(spark_x), int(spark_y)), int(spark_size))
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

# Clase de los Obstáculos
class Asteroid:
    def __init__(self):
        self.radius = random.randint(20, 35)
        self.respawn()
        self.speed = random.uniform(2.0, 6.0)
        self.rotation = 0
        self.rotation_speed = random.uniform(-3.0, 3.0)
        self.create_asteroid_surface()
    
    def create_asteroid_surface(self):
        # Crear superficie para el asteroide con forma irregular
        size = self.radius * 2
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Dibujar asteroide con forma irregular
        points = []
        num_points = random.randint(6, 10)
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            variation = random.uniform(0.6, 1.4)
            point_radius = self.radius * variation
            x = self.radius + math.cos(angle) * point_radius
            y = self.radius + math.sin(angle) * point_radius
            points.append((x, y))
        
        # Color del asteroide
        color_variation = random.randint(70, 130)
        asteroid_color = (color_variation, color_variation // 2, color_variation // 3)
        pygame.draw.polygon(self.surface, asteroid_color, points)
        
        # Detalles de cráteres
        for _ in range(random.randint(2, 5)):
            crater_x = random.randint(5, size - 5)
            crater_y = random.randint(5, size - 5)
            crater_radius = random.randint(4, 10)
            crater_color = (color_variation - 40, color_variation // 2 - 20, color_variation // 3 - 15)
            pygame.draw.circle(self.surface, crater_color, (crater_x, crater_y), crater_radius)
    
    def respawn(self):
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = -self.radius
    
    def update(self):
        self.y += self.speed
        self.rotation += self.rotation_speed
        if self.y > HEIGHT + self.radius:
            self.respawn()
            return True
        return False
    
    def draw(self):
        # Rotar y dibujar el asteroide
        rotated_surface = pygame.transform.rotate(self.surface, self.rotation)
        rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
        screen.blit(rotated_surface, rotated_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

# Efectos de partículas
class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x, y, color=RED, count=20):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 10)
            lifetime = random.randint(30, 60)
            size = random.randint(2, 6)
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'color': color,
                'size': size
            })
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['lifetime'] -= 1
            particle['vy'] += 0.2  # Gravedad más fuerte
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self):
        for particle in self.particles:
            # Calcular alpha basado en vida restante
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            color = particle['color']
            if len(color) == 3:
                color = (*color, alpha)
            
            surf = pygame.Surface((particle['size']*2, particle['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (particle['size'], particle['size']), particle['size'])
            screen.blit(surf, (particle['x'] - particle['size'], particle['y'] - particle['size']))

# Inicializar juego
spaceship = Spaceship()
points = [Point() for _ in range(5)]
asteroids = [Asteroid() for _ in range(6)]
particles = ParticleSystem()
score = 0
game_over = False
spawn_timer = 0

# Fuentes
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

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
            if event.key == pygame.K_r and game_over:
                # Reiniciar juego
                spaceship = Spaceship()
                points = [Point() for _ in range(5)]
                asteroids = [Asteroid() for _ in range(6)]
                particles = ParticleSystem()
                score = 0
                game_over = False
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    if not game_over:
        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()
        
        # Mover nave y obtener si se está moviendo
        is_moving = spaceship.move(keys)
        
        # Actualizar puntos
        for point in points:
            point.update()
            if not point.collected and spaceship.rect.colliderect(point.get_rect()):
                point.collected = True
                score += 10
                particles.add_explosion(point.x, point.y, GREEN, 20)
                # Respawn después de un delay
                pygame.time.set_timer(pygame.USEREVENT + len(points), 1000)
        
        # Actualizar asteroides
        spawn_timer += 1
        if spawn_timer >= 40:  # Cada 0.66 segundos
            asteroids.append(Asteroid())
            spawn_timer = 0
        
        for asteroid in asteroids:
            asteroid.update()
            
            # Verificar colisión con nave
            if spaceship.rect.colliderect(asteroid.get_rect()):
                particles.add_explosion(spaceship.rect.centerx, spaceship.rect.centery, RED, 60)
                game_over = True
        
        # Actualizar partículas
        particles.update()
    
    # Dibujar
    screen.fill(BLACK)
    
    # Dibujar estrellas de fondo animadas
    current_time = pygame.time.get_ticks()
    for i in range(150):
        x = (i * 157) % WIDTH
        y = (i * 233) % HEIGHT
        brightness = 80 + int(70 * math.sin(current_time * 0.0005 + i))
        size = 1 + (i % 3)
        color = (brightness, brightness, min(255, brightness + 50))
        pygame.draw.circle(screen, color, (x, y), size)
    
    # Dibujar puntos
    for point in points:
        point.draw()
    
    # Dibujar asteroides
    for asteroid in asteroids:
        asteroid.draw()
    
    # Dibujar partículas
    particles.draw()
    
    # Dibujar nave (si no hay game over)
    if not game_over:
        spaceship.draw(is_moving)
    
    # Mostrar información
    score_text = font_large.render(f"Puntuación: {score}", True, YELLOW)
    screen.blit(score_text, (10, 10))
    
    # Instrucciones
    if not game_over:
        instructions = [
            "CONTROLES:",
            "Flechas: Mover Nave Slayer",
            "Objetivos: ● Verde = +10 puntos",
            "Peligro: ● Asteroides = Game Over"
        ]
        
        for i, text in enumerate(instructions):
            color = WHITE if i == 0 else (200, 200, 200)
            text_surf = font_small.render(text, True, color)
            screen.blit(text_surf, (10, 60 + i * 25))
    
    if game_over:
        # Fondo semitransparente
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("¡GAME OVER!", True, RED)
        score_final = font_medium.render(f"Puntuación Final: {score}", True, YELLOW)
        restart_text = font_medium.render("Presiona R para reiniciar", True, GREEN)
        quit_text = font_small.render("Presiona ESC para salir", True, WHITE)
        
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
        screen.blit(score_final, (WIDTH//2 - score_final.get_width()//2, HEIGHT//2 - 20))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 30))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 80))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()