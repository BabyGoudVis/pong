import pygame
import sys
import json
import os
from random import *
from math import cos, radians, sin
from time import sleep

FPS = 60
WIDTH, HEIGHT = 1280, 720


WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
VELOCITY = 600  # pixels / s
BASE_BALL_VELOCITY = 300  # pixels / s

pygame.init()
pygame.display.set_caption("pong pong pong!")
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

baseFont = pygame.font.SysFont("Arial", int(HEIGHT / 10))

playButton = pygame.Rect((WIDTH * 0.76875)/2 - 20, HEIGHT / 2 - 20,
                         WIDTH * 0.23125 + 40, int(HEIGHT / 10) + 40)

filename = 'data.json'
with open(filename, 'r') as f:
    data = json.load(f)
    highScore = data['highscore']
    newHighscore = data['newHighscore']


class Platform:
    def __init__(self):
        self.width = WIDTH / 4
        self.height = HEIGHT / 70
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
        self.angle = randint(0, 180)
        self.BaseVelocity = BASE_BALL_VELOCITY / FPS
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
        ball.BaseVelocity = (BASE_BALL_VELOCITY /
                             FPS) ** (1 + (counter // 5) / 5)

    def draw(self):
        pygame.draw.rect(surface, WHITE, self.ball)


def drawing():
    surface.fill(BLACK)
    match status:
        case "home":
            text_surface = baseFont.render(
                f"High Score: {highScore}", True, WHITE)
            surface.blit(text_surface, (WIDTH / 100, HEIGHT / 100))
            text_surface = baseFont.render("New Game", True, WHITE)
            surface.blit(text_surface, ((WIDTH * 0.76875)/2, HEIGHT / 2))
            pygame.draw.rect(surface, WHITE, playButton, 2)
        case "game":
            text_surface = baseFont.render(
                f"Score: {scoreMessage}", True, WHITE)
            surface.blit(text_surface, (WIDTH / 100, HEIGHT / 100))
            platform.draw()
            ball.draw()
        case "game over" | "waiting":
            text_surface = baseFont.render("Game over!", True, WHITE)
            surface.blit(text_surface, (WIDTH / 5, HEIGHT // 4))
            if newHighscore:
                text_surface = baseFont.render(
                    f"Score: {counter}     New High Score!!", True, WHITE)
            else:
                text_surface = baseFont.render(
                    f"Score: {counter}     High Score: {highScore}", True, WHITE)
            surface.blit(text_surface, (WIDTH / 5, HEIGHT // 3))
            text_surface = baseFont.render(
                f"Press space to go to home screen", True, WHITE)
            surface.blit(text_surface, (WIDTH / 5, HEIGHT // 2))

    pygame.display.update()


def getCollition(platform, ball, counter):
    collisionTolerance = ball.BaseVelocity * 1.1
    if ball.ball.left <= 0 or ball.ball.right >= WIDTH:
        ball.angle = 180 - ball.angle - randint(-5, 5)
    if ball.ball.top <= 0:
        ball.angle *= -1
        ball.angle == randint(-5, 5)
    if platform.platform.colliderect(ball.ball):
        if abs(platform.platform.top - ball.ball.bottom) <= collisionTolerance:
            ball.angle *= -1
            counter += 1
        if abs(platform.platform.right - ball.ball.left) <= collisionTolerance:
            ball.angle = 180 - ball.angle
        if abs(platform.platform.left - ball.ball.right) <= collisionTolerance:
            ball.angle = 180 - ball.angle
    if ball.ball.bottom >= HEIGHT:
        return counter, "game over"
    return counter, "game"


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

status = "home"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and status == "home":
            if playButton.collidepoint(event.pos):
                counter = 0
                del ball, platform
                platform = Platform()
                ball = Ball()
                sleep(0.5)
                status = "game"
    match status:
        case "game":
            handleMovementPlatform()
            platform.checkPosition()
            counter, status = getCollition(platform, ball, counter)
            ball.movement(ball.angle)
            scoreMessage = counter
        case "game over":
            scoreMessage = "Game Over"
            with open(filename, 'r') as f:
                data = json.load(f)
                highScore = data['highscore']
                if counter > highScore:
                    data['highscore'] = counter
                    data['newHighscore'] = True
                    highScore = counter
                else:
                    data['newHighscore'] = False
                newHighscore = data['newHighscore']

            os.remove(filename)
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            status = "waiting"
        case "waiting":
            if gameOver():
                status = "home"
    # print(f"Status: {status}")
    drawing()
    clock.tick(FPS)
