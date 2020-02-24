import time
import json
import pygame

from robot import Robot
from snake import Snake

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
w, h = pygame.display.get_surface().get_size()
grid_size = (20, 20)
cell_size = (320 * (w / 400)) / grid_size[0]
offset = (w - (grid_size[0] * (cell_size - 1))) / 2

r = Robot(grid_size)
wins = 0
do_draw = False
run = True
start = True
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)


def draw(snake, apple, score):
    screen.fill((255, 255, 255))

    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            pygame.draw.rect(screen, (0, 0, 0),
                             (x * (cell_size - 1) + offset, y * (cell_size - 1) + offset, cell_size, cell_size), 1)

    pygame.draw.rect(screen,
                     (255, 0, 0),
                     (apple[0] * (cell_size - 1) + offset + 1,
                      apple[1] * (cell_size - 1) + offset + 1,
                      cell_size - 2,
                      cell_size - 2))

    for part in snake:
        pygame.draw.rect(screen, (0, 255, 0), (part[0] * (cell_size - 1) + offset + 1,
                                               part[1] * (cell_size - 1) + offset + 1,
                                               cell_size - 2, cell_size - 2), 0)

    pygame.draw.rect(screen, (0, 0, 0), (snake[0][0] * (cell_size - 1) + offset + 1,
                                           snake[0][1] * (cell_size - 1) + offset + 1,
                                           cell_size - 2, cell_size - 2), 1)

    textsurface = font.render('Score: ' + str(score), False, (0, 0, 0))
    screen.blit(textsurface, (0, 0))

    pygame.display.flip()


screen.fill((255, 255, 255))

textsurface = font.render('Press Y to use the Q-table of previous learning fase,', False, (0, 0, 0))
screen.blit(textsurface, (0, 0))
textsurface = font.render('Press N to start a new learning fase', False, (0, 0, 0))
screen.blit(textsurface, (0, 100))

pygame.display.flip()

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_y:
                with open('q.json', 'r') as inf:
                    r.q = eval(inf.read())
                start = False
            if event.key == pygame.K_n:
                start = False

print(r.q)

screen.fill((255, 255, 255))

textsurface = font.render('Press Y to have the AI know all of it trail parts (Takes long),', False, (0, 0, 0))
screen.blit(textsurface, (0, 0))
textsurface = font.render('Press N to have the AI only know its last trail part (Quick, not perfect) ', False, (0, 0, 0))
screen.blit(textsurface, (0, 100))

pygame.display.flip()

start = True

while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_y:
                r.trail = True
                start = False
            if event.key == pygame.K_n:
                r.trail = False
                start = False

screen.fill((255, 255, 255))

pygame.display.flip()

print(r.trail)

while run:
    s = Snake(grid_size, r)
    wonThisTurn = False
    i = 0
    while s.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    do_draw = not do_draw
                if event.key == pygame.K_r:
                    s.running = False
                if event.key == pygame.K_s:
                    data = json.dumps(r.q)
                    f = open("q.json", "w")
                    f.write(data)
                    f.close()
                    s.running = False
                    run = False

        i += 1
        s.parse_events()
        if s.score > 15:
            wonThisTurn = True
            wins += 1
            s.running = False
        if i > 1000 and wins < 20:
            print("reset")
            s.running = False
        if s.reset:
            s.running = False
        if do_draw:
            draw(s.snake, s.apple, s.score)
            time.sleep(0.1)
