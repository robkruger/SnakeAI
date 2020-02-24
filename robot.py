import random

import numpy as np


class Robot(object):

    def __init__(self, grid_size):
        self.num_actions = 4
        self.epsilon = 0.05
        self.alpha = 0.85
        self.gamma = 0.9

        self.q = {}
        self.state = "(0, 0), (0, 0)"
        self.q[self.state] = [0.0, 0.0, 0.0, 0.0]
        self.action = 0
        self.total_reward = 0
        # Determines if the AI knows the position of the whole trail or only the last element
        self.trail = False

    def do_action(self, apple, snake):
        self.state = str(apple[0] - snake[0][0]) + str(apple[1] - snake[0][1])
        if self.trail:
            for i in range(1, len(snake)):
                self.state += str(snake[i][0] - snake[0][0]) + str(snake[i][1] - snake[0][1])
        else:
            self.state += str(snake[-1][0] - snake[0][0]) + str(snake[-1][1] - snake[0][1])
        if self.state not in self.q:
            self.q[self.state] = [0.0, 0.0, 0.0, 0.0]
        if random.uniform(0, 1) < self.epsilon:
            self.action = random.choice(range(4))
        else:
            self.action = np.argmax(self.q[self.state])
        return self.action

    def update(self, reward, apple, snake):
        self.total_reward += reward
        new_state = str(apple[0] - snake[0][0]) + str(apple[1] - snake[0][1])
        if self.trail:
            for i in range(1, len(snake)):
                new_state += str(snake[i][0] - snake[0][0]) + str(snake[i][1] - snake[0][1])
        else:
            new_state += str(snake[-1][0] - snake[0][0]) + str(snake[-1][1] - snake[0][1])
        if new_state not in self.q:
            self.q[new_state] = [0.0, 0.0, 0.0, 0.0]
        old_value = self.q[self.state][self.action]
        next_max = np.max(self.q[new_state])

        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q[self.state][self.action] = new_value

        self.state = new_state
