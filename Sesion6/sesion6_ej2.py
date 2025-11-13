import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recolección de Objetos")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Jugador
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5

# Objetos a recolectar
class Collectible:
    def __init__(self):
        self.radius = 15
        self.respawn()
    
    def respawn(self):
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius, 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

# Crear objetos
collectibles = [Collectible() for _ in range(5)]
score = 0

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
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed
    
    # Crear rectángulo del jugador
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    # Verificar colisiones con objetos
    for collectible in collectibles[:]:
        if player_rect.colliderect(collectible.get_rect()):
            collectible.respawn()
            score += 1
            print(f"¡Objeto recolectado! Puntos: {score}")
    
    # Dibujar
    screen.fill(WHITE)
    
    # Dibujar objetos
    for collectible in collectibles:
        collectible.draw()
    
    # Dibujar jugador
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, (0, 0, 0), (player_x, player_y, player_size, player_size), 2)
    
    # Mostrar información
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Puntos: {score}", True, (0, 0, 0))
    info_text = font.render("Recolecta los círculos de colores", True, (0, 0, 0))
    
    screen.blit(score_text, (10, 10))
    screen.blit(info_text, (10, HEIGHT - 50))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()