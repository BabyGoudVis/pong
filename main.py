import pygame
import sys
from random import *
from math import cos, radians, sin
from time import sleep

FPS = 60
WIDTH, HEIGHT = 1280, 720


WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
VELOCITY = WIDTH / 2  # xCord moves 600/s
BASE_BALL_VELOCITY = 300 / FPS

pygame.init()
pygame.display.set_caption("pong pong pong!")
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

baseFont = pygame.font.SysFont("Arial", int(HEIGHT / 10))


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
        self.BaseVelocity = BASE_BALL_VELOCITY
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
        ball.BaseVelocity = BASE_BALL_VELOCITY ** (1 + (counter // 5) / 5)

    def draw(self):
        pygame.draw.rect(surface, WHITE, self.ball)


def drawing():
    surface.fill(BLACK)
    platform.draw()
    ball.draw()

    if counter < 0:
        text_surface = baseFont.render(f"Game over: {endScore}", True, WHITE)
        surface.blit(text_surface, (WIDTH / 3, HEIGHT / 3))
        text_surface = baseFont.render(
            f"Press space to play again", True, WHITE)
        surface.blit(text_surface, (WIDTH / 3, HEIGHT / 2))
    else:
        text_surface = baseFont.render(f"Score: {scoreMessage}", True, WHITE)
        surface.blit(text_surface, (WIDTH / 100, HEIGHT / 100))
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
        if abs(platform.platform.right - ball.ball.left) <= collisionTolerance:
            ball.angle = 180 - ball.angle
        if abs(platform.platform.left - ball.ball.right) <= collisionTolerance:
            ball.angle = 180 - ball.angle
    if ball.ball.bottom >= HEIGHT:
        endScore = counter
        return -1, endScore
    endScore = counter
    return counter, counter


def handleMovementPlatform():
    leftPressed = False
    rightPressed = False
    if pygame.key.get_pressed()[pygame.K_q] or pygame.key.get_pressed()[pygame.K_LEFT]:
        leftPressed = True
    if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
        rightPressed = True
    if not (leftPressed and rightPressed):
        if leftPressed:
            platform.platform.x -= platform.velocity
        elif rightPressed:
            platform.platform.x += platform.velocity

    if pygame.mouse.get_pressed()[0]:
        xMouse, yMouse = pygame.mouse.get_pos()
        platform.platform.x = xMouse - platform.width / 2


def gameOver():
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        return True
    return False


platform = Platform()
ball = Ball()
counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    if counter < 0:
        scoreMessage = "Game Over"
        if gameOver():
            sleep(1)
            counter = 0
            del ball, platform
            platform = Platform()
            ball = Ball()
    else:
        handleMovementPlatform()
        platform.checkPosition()
        counter, endScore = getCollition(platform, ball, counter)
        ball.movement(ball.angle)
        scoreMessage = counter
    drawing()
    clock.tick(FPS)
