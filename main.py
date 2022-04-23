from operator import length_hint
import pygame
from pygame.locals import *
import time
import random
import logging

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/apple.jpg").convert()
        self.x = random.randint(20, X_SIZE-20)
        self.y = random.randint(20, Y_SIZE-20)

    def draw(self):
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 25)*SIZE
        self.y = random.randint(1, 20)*SIZE
        self.draw()


class Snake:
    # assigning key function for going up, down, left, right
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("./resources/block.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.x = [40]*length
        self.y = [40]*length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # change body
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    # background color: pink
    def draw(self):
        self.parent_screen.fill((23, 156, 34))

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

# the windown thing


class Game:
    #change length of snake to 1 so score can be 1
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((X_SIZE, Y_SIZE))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def invert_direction(self):
        if self.snake.direction == 'left':
            logging.debug("moving right")
            self.snake.move_right()
            return
        if self.snake.direction == 'right':
            logging.debug("moving left")
            self.snake.move_left()
            return
        if self.snake.direction == 'up':
            logging.debug("moving down")
            self.snake.move_down()
            return
        if self.snake.direction =='down':
            logging.debug("moving up")
            self.snake.move_up()
            return


    def check_boundary(self, x1, y1, OUTSIDE):
        if (x1 <= 0 or x1 > X_SIZE) and OUTSIDE == 0:
            logging.debug("Inverting X direction [%s]", x1)
            self.invert_direction()
            OUTSIDE = 1
        elif x1 > 0 or x1 < X_SIZE:
            logging.debug("Resetting OUTSIDE for X")
            OUTSIDE = 0
        if (y1 <= 0 or y1 > Y_SIZE) and OUTSIDE == 0:
            logging.debug("Inverting Y direction [%s]", y1)
            self.invert_direction()
            OUTSIDE = 1
        elif y1 > 0 or y1 < Y_SIZE:
            logging.debug("Resetting OUTSIDE for Y")
            OUTSIDE = 0
        return OUTSIDE
#scoreboard        
    def display_Score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))
        

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_Score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            logging.debug("COLLISION, snake[%s, %s], apple[%s, %s], snake before length[%s]",
                          self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y, self.snake.length)
            self.snake.increase_length()
            logging.debug("After increase length, snake new length[%s]", self.snake.length)
            logging.debug("BEFORE apple move, apple[%s, %s]", self.apple.x, self.apple.y)
            self.apple.move()
            logging.debug("AFTER apple move, apple[%s, %s]", self.apple.x, self.apple.y)
        else:
            logging.debug("No collision, snake[%s, %s], apple[%s, %s]", self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y)


    def run(self):
        running = True
        OUTSIDE = 0

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            OUTSIDE = self.check_boundary(self.snake.x[0], self.snake.y[0], OUTSIDE)
            logging.debug("Value of OUTSIDE[%s]", OUTSIDE)
            self.play()

            time.sleep(.2)


if __name__ == "__main__":
    # Change the logging level below from DEBUG to INFO when you are finished
    # Please remove game.log each time you run, or you will fill up your disc!
    logging.basicConfig(filename='game.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    SIZE = 40
    X_SIZE = 1000
    Y_SIZE = 800
    game = Game()
    game.run()