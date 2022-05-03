# Asteroiden bewegen sich nach unten, Player bleibt auf Pixel stehen (wandert nicht mit nach unten)
import pygame
import numpy
from recordtype import recordtype
from enum import Enum

pygame.init()


# Directions
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


# Player
Point = recordtype('Point', 'x, y')

asteroidProbability = 0.9

# RGB Colors
RED = (200, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 2


def _generateRow():
    pixelRow = []
    for x in range(0, 10):
        if numpy.random.choice([0, 1], p=[asteroidProbability, 1 - asteroidProbability]) == 1:
            new_asteroid = Point(x, 0)
            pixelRow.append(new_asteroid)
    return pixelRow


def _generateAsteroids():
    asteroids = []
    for x in range(0, 10):
        new_row = _generateRow()
        for asteroid in range(len(new_row)):
            new_row[asteroid].y = x
        asteroids.append(new_row)
    return asteroids


def _setAsteroidsDown(asteroids):
    for asteroidRow in asteroids:
        for asteroid in asteroidRow:
            asteroid.y += 1
    return asteroids


class AsteroidGame:
    def __init__(self, w=200, h=200):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Asteroids')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # Player in middle
        self.player = Point(5, 5)
        # Generate Asteroids
        self.asteroids = _generateAsteroids()

        # Init variables
        self.score = 0
        self.frame_iteration = 0

    def play_step(self, action):
        self.frame_iteration += 1
        # Check if Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move
        self._move(action)

        # Check if GameOver
        game_over = False
        reward = 0

        if self.is_collision():
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # Return reward, gameover, score
        return reward, game_over, self.score

    def is_collision(self):
        print(self.player.x, self.player.y)
        # Hits Boundary
        if self.player.x + 1 > self.w / BLOCK_SIZE or self.player.x < 0 or self.player.y + 1 > self.h / BLOCK_SIZE or self.player.y < 0:
            return True
        # Hits Asteroid
        for asteroidRow in self.asteroids:
            for asteroid in asteroidRow:
                if asteroid.x == self.player.x:
                    if asteroid.y == self.player.y:
                        return True

    def _move(self, action=None):
        # Set Asteroids 1 down
        self.asteroids = _setAsteroidsDown(self.asteroids)
        self.asteroids.pop()
        self.asteroids.insert(0, _generateRow())

        # Move Player
        if action:
            if action == Direction.RIGHT:
                self.player.x += 1
            elif action == Direction.LEFT:
                self.player.x -= 1
            elif action == Direction.UP:
                self.player.y -= 1
            else:  # Direction.DOWN
                self.player.y += 1

    def _update_ui(self):
        self.display.fill(WHITE)

        # Draw Asteroids
        for asteroidRow in self.asteroids:
            for asteroid in asteroidRow:
                pygame.draw.rect(self.display, BLACK, pygame.Rect(asteroid.x * BLOCK_SIZE, asteroid.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw Player
        pygame.draw.rect(self.display, RED, pygame.Rect(self.player.x * BLOCK_SIZE, self.player.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()


if __name__ == '__main__':
    game = AsteroidGame()
    action = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    action = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    action = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    action = Direction.UP
                elif event.key == pygame.K_DOWN:
                    action = Direction.DOWN
            else:
                action = None
        reward, game_over, score = game.play_step(action)
        if game_over:
            break
        # time.sleep(2)
    print(score)
