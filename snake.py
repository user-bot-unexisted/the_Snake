
import sys
import random
import pygame
from pygame.math import Vector2  # type: ignore[attr-defined]

FRUIT_COLOR = (126, 166, 114)
FRUIT_SIZE = 20

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Fruits:
    """Fruta del juego. Se posiciona aleatoriamente evitando la serpiente."""
    def __init__(self) -> None:
        self.position = Vector2(0, 0)
        self.randomize([])
    def draw(self):
        rect = pygame.Rect(int(self.position.x), int(self.position.y), FRUIT_SIZE, FRUIT_SIZE)
        pygame.draw.rect(screen, FRUIT_COLOR, rect)
    def randomize(self, occupied_positions):
        while True:
            x = random.randrange(0, SCREEN_WIDTH, FRUIT_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, FRUIT_SIZE)
            candidate = Vector2(x, y)
            if candidate not in occupied_positions:
                self.position = candidate
                return

class Snake:
    """Serpiente controlada por el jugador."""
    def __init__(self) -> None:
        self.body = [Vector2(100, 100), Vector2(120, 100), Vector2(140, 100)]
        self.direction = Vector2(1, 0)
        self.new_block = False
    def draw(self):
        for score in self.body:
            x_pos = int(score.x)
            y_pos = int(score.y)
            groth = pygame.Rect(x_pos, y_pos, FRUIT_SIZE, FRUIT_SIZE)
            pygame.draw.rect(screen, ('yellow'), groth)
    def move(self):
        new_head = self.body[0] + self.direction * FRUIT_SIZE
        if new_head.x >= SCREEN_WIDTH:
            new_head.x = 0
        elif new_head.x < 0:
            new_head.x = SCREEN_WIDTH - FRUIT_SIZE
        if new_head.y >= SCREEN_HEIGHT:
            new_head.y = 0
        elif new_head.y < 0:
            new_head.y = SCREEN_HEIGHT - FRUIT_SIZE
        if self.new_block:
            self.body = [new_head] + self.body
            self.new_block = False
        else:
            self.body = [new_head] + self.body[:-1]



pygame.init()  


WHITE = (255, 255, 255)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
# si la serpiente no choca no muere y si no muere el juego sigue

# creamos la serpiente


death = False

# mientras no esté muerto el juego sigue

# ya existe la creación de frutas así que ahora debemos implementarla

fruit = Fruits()
snake = Snake()

SCREEN_UPDATE = pygame.USEREVENT  
pygame.time.set_timer(SCREEN_UPDATE, 150)
while not death:
    #mantiene la pantalla activa
    for event in pygame.event.get():
        #si no se quiere seguir se puede cerrar
        if event.type == pygame.QUIT:  
            pygame.quit()  
            sys.exit()
        if event.type == SCREEN_UPDATE:
            snake.move()
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_UP and snake.direction.y != 1:  
                snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and snake.direction.y != -1:  
                snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT and snake.direction.x != 1:  
                snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and snake.direction.x != -1:  
                snake.direction = Vector2(1, 0)
    # hacemos que no se vaya tan rápido, mantener velocidad constante

    #la pantalla ahora es blanca
    # check if snake eats the fruit
    if snake.body[0].x == fruit.position.x and snake.body[0].y == fruit.position.y:
        snake.new_block = True
        fruit.randomize(snake.body)

    screen.fill(WHITE)
    fruit.draw()
    snake.draw()
    #actualiza los fps
    pygame.display.update()
    #mantiene los fps en 60
    clock.tick(60)
    