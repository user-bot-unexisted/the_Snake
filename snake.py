
from pyclbr import Class
from numpy import full
import pygame,sys,random
from pygame.math import Vector2 as vector2  # type: ignore[attr-defined]

FRUIT_COLOR = (126, 166, 114)
FRUIT_SIZE = 20

cell_size = 800 
cell_number = 600
class Fruits():
    def __init__(self) -> None:
        # start at a random grid-aligned position
        self.position = vector2(0, 0)
        self.randomize([])
    def appears(self):
        rect = pygame.Rect(int(self.position.x), int(self.position.y), FRUIT_SIZE, FRUIT_SIZE)
        pygame.draw.rect(screen,FRUIT_COLOR,rect)
    def randomize(self, occupied_positions):
        # choose a random grid cell not occupied by the snake
        while True:
            x = random.randrange(0, cell_size, FRUIT_SIZE)
            y = random.randrange(0, cell_number, FRUIT_SIZE)
            candidate = vector2(x, y)
            if candidate not in occupied_positions:
                self.position = candidate
                return

class Snake():
    def __init__(self) -> None:
        self.body = [vector2(100,100), vector2(120,100), vector2(140,100)]
        self.direction = vector2(1,0)
        self.new_block = False
    def grown(self):
        for score in self.body:
            x_pos = int(score.x)
            y_pos = int(score.y)
            groth = pygame.Rect(x_pos, y_pos, FRUIT_SIZE, FRUIT_SIZE)
            pygame.draw.rect(screen,('yellow'),groth)
    def movement(self):
        new_head = self.body[0] + self.direction * FRUIT_SIZE
        if new_head.x >= cell_size:
            new_head.x = 0
        elif new_head.x < 0:
            new_head.x = cell_size - FRUIT_SIZE
        if new_head.y >= cell_number:
            new_head.y = 0
        elif new_head.y < 0:
            new_head.y = cell_number - FRUIT_SIZE
        if self.new_block:
            self.body = [new_head] + self.body
            self.new_block = False
        else:
            self.body = [new_head] + self.body[:-1]
    #ahora que trague la perr
    def collition(self):
        pass


pygame.init()  # type: ignore[attr-defined]


WHITE = (255, 255, 255)


screen = pygame.display.set_mode((cell_size,cell_number))

clock = pygame.time.Clock()
#si la serpiente no choca no mere y si no muere el juego sigue

#creamos la serpiente


death = False

#mientras no este muerto el juego sigue

#ya existe la creaciion ded frutas asi que ahora debemos implementarla

fruit = Fruits()
snake = Snake()

scree_update = pygame.USEREVENT  # type: ignore[attr-defined]
pygame.time.set_timer(scree_update,150)
while not death:
    #mantiene la pantalla activa
    for event in pygame.event.get():
#si no se quiere seguir se puede cerrar
        if event.type == pygame.QUIT:  # type: ignore[attr-defined]
            pygame.quit()  # type: ignore[attr-defined]
            sys.exit()
        if event.type == scree_update:
            snake.movement()
        if event.type == pygame.KEYDOWN:  # type: ignore[attr-defined]
            if event.key == pygame.K_UP and snake.direction.y != 1:  # type: ignore[attr-defined]
                snake.direction = vector2(0,-1)
            elif event.key == pygame.K_DOWN and snake.direction.y != -1:  # type: ignore[attr-defined]
                snake.direction = vector2(0,1)
            elif event.key == pygame.K_LEFT and snake.direction.x != 1:  # type: ignore[attr-defined]
                snake.direction = vector2(-1,0)
            elif event.key == pygame.K_RIGHT and snake.direction.x != -1:  # type: ignore[attr-defined]
                snake.direction = vector2(1,0)
    #hacems que no se vaya verguiado volao sino que se vaya lento

    #la pantalla ahora es blanca
    # check if snake eats the fruit
    if snake.body[0].x == fruit.position.x and snake.body[0].y == fruit.position.y:
        snake.new_block = True
        fruit.randomize(snake.body)

    screen.fill(WHITE)
    fruit.appears()
    snake.grown()
    #actualiza los fps
    pygame.display.update()
    #mantiene los fps en 60
    clock.tick(60)
    