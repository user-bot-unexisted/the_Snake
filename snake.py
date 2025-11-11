
import sys
import random
import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    USEREVENT,
)
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

    def draw(self) -> None:
        rect = pygame.Rect(
            int(self.position.x),
            int(self.position.y),
            FRUIT_SIZE,
            FRUIT_SIZE,
        )
        pygame.draw.rect(screen, FRUIT_COLOR, rect)

    def randomize(self, occupied_positions) -> None:
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

    def draw(self) -> None:
        for score in self.body:
            x_pos = int(score.x)
            y_pos = int(score.y)
            groth = pygame.Rect(x_pos, y_pos, FRUIT_SIZE, FRUIT_SIZE)
            pygame.draw.rect(screen, ("yellow"), groth)

    def move(self) -> None:
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


def handle_event(event: pygame.event.Event, snake_obj: Snake) -> None:
    """Procesa eventos y actualiza la dirección o estado."""
    if event.type == QUIT:
        pygame.quit()  # type: ignore[attr-defined]
        sys.exit()
    if event.type == SCREEN_UPDATE:
        snake_obj.move()
    if event.type == KEYDOWN:
        if event.key == K_UP and snake_obj.direction.y != 1:
            snake_obj.direction = Vector2(0, -1)
        elif event.key == K_DOWN and snake_obj.direction.y != -1:
            snake_obj.direction = Vector2(0, 1)
        elif event.key == K_LEFT and snake_obj.direction.x != 1:
            snake_obj.direction = Vector2(-1, 0)
        elif event.key == K_RIGHT and snake_obj.direction.x != -1:
            snake_obj.direction = Vector2(1, 0)


def check_eat(snake_obj: Snake, fruit_obj: Fruits) -> None:
    """Comprueba si la serpiente come la fruta y la reubica."""
    head = snake_obj.body[0]
    if head.x == fruit_obj.position.x and head.y == fruit_obj.position.y:
        snake_obj.new_block = True
        fruit_obj.randomize(snake_obj.body)


pygame.init()

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

death = False

# Ya existe la creación de frutas así que ahora debemos implementarla
fruit = Fruits()
snake = Snake()

SCREEN_UPDATE = USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
while not death:
    # Mantiene la pantalla activa
    for event in pygame.event.get():
        handle_event(event, snake)

    # La pantalla ahora es blanca y verificamos si come
    check_eat(snake, fruit)

    screen.fill(WHITE)
    fruit.draw()
    snake.draw()
    # Actualizasddiigr
    pygame.display.update()
    # Mantiene los fps en 60
    clock.tick(60)