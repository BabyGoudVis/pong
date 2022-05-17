import pygame
import sys
from random import *
from math import cos, radians, sin

from pyrsistent import b
FPS = 60
WIDTH, HEIGHT = 1280, 720


WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
VELOCITY = 600  # xCord moves 600/s

pygame.init()
pygame.display.set_caption("pong pong pong!")
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Platform:
    def __init__(self):
        self.width = WIDTH / 5
        self.height = HEIGHT / 50
        self.x = (WIDTH - self.width) / 2
        self.y = (HEIGHT / 5) * 4
        self.velocity = VELOCITY / FPS
        self.platform = pygame.Rect(self.x, self.y, self.width, self.height)

    def checkPosition(self):
        if platform.platform.x < 0:
            platform.platform.x = 0
        if platform.platform.x + platform.width > WIDTH:
            platform.platform.x = WIDTH - platform.width

    def draw(self):
        pygame.draw.rect(surface, WHITE, self.platform)


class Ball:
    def __init__(self):
        self.radius = 10
        self.x = WIDTH / 2
        self.y = HEIGHT / 5
        self.angle = 160
        self.BaseVelocity = 10
        self.xVelocity = 0
        self.yVelocity = 0
        self.ball = pygame.Rect(self.x, self.y, self.radius, self.radius)

    def movement(self, angle):
        ball.xVelocity = cos(radians(angle)) * ball.BaseVelocity
        ball.yVelocity = sin(radians(angle)) * ball.BaseVelocity
        ball.ball.x += ball.xVelocity
        ball.ball.y -= ball.yVelocity
        if ball.angle >= 360:
            ball.angle -= 360
        if ball.angle < 0:
            ball.angle += 360

    def draw(self):
        pygame.draw.rect(surface, WHITE, self.ball)


def drawing():
    surface.fill(BLACK)
    platform.draw()
    ball.draw()
    pygame.display.update()


def getCollition(platform, ball, counter):
    collisionTolerance = 5
    if ball.ball.left <= 0 or ball.ball.right >= WIDTH:
        ball.angle = 180 - ball.angle
    if ball.ball.top <= 0:
        ball.angle *= -1
    if platform.platform.colliderect(ball.ball):
        if abs(platform.platform.top - ball.ball.bottom) <= collisionTolerance:
            ball.angle *= -1
            counter += 1
    if ball.ball.bottom >= HEIGHT:
        return "LOST"
    return counter


platform = Platform()
ball = Ball()
counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if pygame.key.get_pressed()[pygame.K_d]:
        platform.platform.x += platform.velocity
    if pygame.key.get_pressed()[pygame.K_q]:
        platform.platform.x -= platform.velocity
    platform.checkPosition()
    counter = getCollition(platform, ball, counter)
    print(counter)
    ball.movement(ball.angle)
    drawing()
    clock.tick(FPS)
