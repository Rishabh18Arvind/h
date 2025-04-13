import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game window
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Player car
class PlayerCar:
    def __init__(self):
        self.width = 50
        self.height = 100
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 5
        
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        
    def move(self, direction):
        if direction == "left" and self.x > 50:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width - 50:
            self.x += self.speed

# Opponent cars
class OpponentCar:
    def __init__(self):
        self.width = 50
        self.height = 100
        self.x = random.choice([150, 350, 550])
        self.y = -self.height
        self.speed = random.randint(3, 7)
        
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        
    def move(self):
        self.y += self.speed
        return self.y > HEIGHT

# Road
def draw_road():
    pygame.draw.rect(screen, GRAY, (50, 0, WIDTH - 100, HEIGHT))
    # Road markings
    for i in range(0, HEIGHT, 50):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, i, 10, 30))

# Game variables
player = PlayerCar()
opponents = []
score = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
game_over = False

# Game loop
running = True
while running:
    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
            
        # Spawn opponents
        if random.random() < 0.02:
            opponents.append(OpponentCar())
            
        # Move opponents and check collisions
        for opponent in opponents[:]:
            if opponent.move():
                opponents.remove(opponent)
                score += 1
            # Collision detection
            if (player.x < opponent.x + opponent.width and
                player.x + player.width > opponent.x and
                player.y < opponent.y + opponent.height and
                player.y + player.height > opponent.y):
                game_over = True
    
    # Drawing
    screen.fill(BLACK)
    draw_road()
    player.draw()
    for opponent in opponents:
        opponent.draw()
        
    # Score display
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    if game_over:
        game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            player = PlayerCar()
            opponents = []
            score = 0
    
    pygame.display.update()

pygame.quit()
