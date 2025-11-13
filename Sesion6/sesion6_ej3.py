import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evitar Obstáculos")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Jugador
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 20
player_speed = 6

# Obstáculos
class Obstacle:
    def __init__(self):
        self.radius = random.randint(15, 30)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = -self.radius
        self.speed = random.randint(3, 7)
        self.color = (random.randint(100, 255), random.randint(50, 150), random.randint(50, 150))
    
    def update(self):
        self.y += self.speed
        return self.y > HEIGHT + self.radius  # Retorna True si salió de la pantalla
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius, 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

# Variables del juego
obstacles = []
spawn_timer = 0
game_over = False
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reiniciar juego
                obstacles = []
                player_x = WIDTH // 2 - player_size // 2
                player_y = HEIGHT - player_size - 20
                game_over = False
                score = 0
    
    if not game_over:
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
        
        # Generar nuevos obstáculos
        spawn_timer += 1
        if spawn_timer >= 30:  # Cada medio segundo aproximadamente
            obstacles.append(Obstacle())
            spawn_timer = 0
        
        # Actualizar obstáculos
        for obstacle in obstacles[:]:
            if obstacle.update():
                obstacles.remove(obstacle)
                score += 1
        
        # Crear rectángulo del jugador
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        
        # Verificar colisiones
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.get_rect()):
                game_over = True
    
    # Dibujar
    screen.fill(WHITE)
    
    # Dibujar obstáculos
    for obstacle in obstacles:
        obstacle.draw()
    
    # Dibujar jugador
    player_color = RED if game_over else BLUE
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size), 2)
    
    # Mostrar información
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Puntos: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    if game_over:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("¡GAME OVER!", True, RED)
        restart_text = font.render("Presiona R para reiniciar", True, BLACK)
        
        screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
        screen.blit(restart_text, (WIDTH//2 - 120, HEIGHT//2 + 50))
    else:
        info_text = font.render("Usa las flechas para esquivar los obstáculos", True, BLACK)
        screen.blit(info_text, (10, HEIGHT - 40))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()