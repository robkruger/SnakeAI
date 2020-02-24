import random
import time
from random import randrange
from robot import Robot

import pygame


class Snake(object):

    def __init__(self, grid_size, robot):
        self.running = True
        self.grid_size = grid_size
        self.apple = (randrange(self.grid_size[0]), randrange(self.grid_size[1]))
        self.snake = [(grid_size[0] / 2, grid_size[1] / 2), (grid_size[0] / 2 + 1, grid_size[1] / 2), (grid_size[0] / 2 + 2, grid_size[1] / 2)]
        self.direction = random.choice(range(4))
        self.robot = robot
        self.score = 0
        self.reset = False

    def parse_events(self):
        reward = -0.1

        self.direction = self.robot.do_action(self.apple, self.snake)

        for i in reversed(range(1, len(self.snake))):
            self.snake[i] = self.snake[i - 1]

        if self.direction == 0:
            self.snake[0] = (self.snake[0][0] - 1, self.snake[0][1])
        elif self.direction == 1:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] - 1)
        elif self.direction == 2:
            self.snake[0] = (self.snake[0][0] + 1, self.snake[0][1])
        elif self.direction == 3:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] + 1)

        for i in range(len(self.snake)):
            for j in range(len(self.snake)):
                if i == j:
                    continue
                if self.snake[i] == self.snake[j]:
                    reward = -1
                    self.reset = True

        if self.snake[0][0] < 0 or self.snake[0][0] > self.grid_size[0] - 1:
            reward = -1
            self.reset = True

        if self.snake[0][1] < 0 or self.snake[0][1] > self.grid_size[1] - 1:
            reward = -1
            self.reset = True

        if self.snake[0] == self.apple:
            self.apple = (randrange(self.grid_size[0]), randrange(self.grid_size[1]))
            same_location = True
            while same_location:
                continue_while = False
                for part in self.snake:
                    if part == self.apple:
                        self.apple = (randrange(self.grid_size[0]), randrange(self.grid_size[1]))
                        continue_while = True
                if not continue_while:
                    same_location = False
            self.score += 1
            reward = 1
            if self.direction == 0:
                self.snake.append((self.snake[-1][0] + 1, self.snake[-1][1]))
            elif self.direction == 1:
                self.snake.append((self.snake[-1][0], self.snake[-1][1] - 1))
            elif self.direction == 2:
                self.snake.append((self.snake[-1][0] - 1, self.snake[-1][1]))
            elif self.direction == 3:
                self.snake.append((self.snake[-1][0], self.snake[-1][1] + 1))

        self.robot.update(reward, self.apple, self.snake)
