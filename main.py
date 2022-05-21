import pygame
import sys
import json
import os
from random import *
from math import cos, radians, sin
from time import sleep

WHITE = (255, 255, 255)
BLACK = (25, 25, 25)


class Game:
    FPS = 60
    WIDTH = 1280
    HEIGHT = 720
    clock = pygame.time.Clock()

    @staticmethod
    def get_fps():
        return Game.FPS

    @staticmethod
    def get_width():
        return Game.WIDTH

    @staticmethod
    def get_height():
        return Game.HEIGHT


class Platform:
    def __init__(self):
        self.WIDTH = Game.WIDTH / 4
        self.HEIGHT = Game.HEIGHT / 70
        self.x = (Game.WIDTH - self.WIDTH) / 2
        self.y = (Game.HEIGHT / 5) * 4
        self.velocity = 600 / Game.FPS
        self.platform = pygame.Rect(
            self.x, self.y, self.WIDTH, self.HEIGHT)

    def checkPosition(self):
        if platform.platform.x < 0:
            platform.platform.x = 0
        if platform.platform.x + platform.WIDTH > Game.WIDTH:
            platform.platform.x = Game.WIDTH - platform.WIDTH

    def draw(self):
        pygame.draw.rect(surface, WHITE, self.platform)


class Ball:
    BASE_BALL_VELOCITY = 300

    def __init__(self):
        self.radius = 10
        self.x = Game.WIDTH / 2
        self.y = Game.HEIGHT / 5
        # self.angle = randint(0, 180)
        self.angle = 90
        self.BaseVelocity = Ball.BASE_BALL_VELOCITY / Game.FPS
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
        ball.BaseVelocity = (Ball.BASE_BALL_VELOCITY /
                             Game.FPS) ** (1 + (counter // 5) / 5)
        if ball.BaseVelocity > (Ball.BASE_BALL_VELOCITY / Game.FPS) ** 2:
            ball.BaseVelocity = (Ball.BASE_BALL_VELOCITY / Game.FPS) ** 2

    def draw(self):
        pygame.draw.rect(surface, WHITE, self.ball)


platform = Platform()
ball = Ball()
game = Game()


pygame.init()
pygame.display.set_caption("pong pong pong!")
surface = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))


baseFont = pygame.font.SysFont("Arial", int(Game.HEIGHT / 10))

playButton = pygame.Rect((Game.WIDTH * 0.76875)/2 - 20, Game.HEIGHT / 2 - 20,
                         Game.WIDTH * 0.23125 + 40, int(Game.HEIGHT / 10) + 40)

filename = 'data.json'
with open(filename, 'r') as f:
    data = json.load(f)
    highScore = data['highscore']
    newHighscore = data['newHighscore']


def drawing():
    surface.fill(BLACK)
    match status:
        case "home":
            text_surface = baseFont.render(
                f"High Score: {highScore}", True, WHITE)
            surface.blit(text_surface, (Game.WIDTH / 100, Game.HEIGHT / 100))
            text_surface = baseFont.render("New Game", True, WHITE)
            surface.blit(
                text_surface, ((Game.WIDTH * 0.76875)/2, Game.HEIGHT / 2))
            pygame.draw.rect(surface, WHITE, playButton, 2)
        case "game":
            scoreText = baseFont.render(
                f"Score: {scoreMessage}", True, WHITE)
            surface.blit(scoreText, (Game.WIDTH / 100, Game.HEIGHT / 100))
            debugText = baseFont.render(
                f"Velocity: {ball.BaseVelocity}", True, (50, 50, 50))
            surface.blit(debugText, (Game.WIDTH /
                         100, Game.HEIGHT / 100 + 72))
            platform.draw()
            ball.draw()
        case "game over" | "waiting":
            text_surface = baseFont.render("Game over!", True, WHITE)
            surface.blit(text_surface, (Game.WIDTH / 5, Game.HEIGHT // 4))
            if newHighscore:
                text_surface = baseFont.render(
                    f"Score: {counter}     New High Score!!", True, WHITE)
            else:
                text_surface = baseFont.render(
                    f"Score: {counter}     High Score: {highScore}", True, WHITE)
            surface.blit(text_surface, (Game.WIDTH / 5, Game.HEIGHT // 3))
            text_surface = baseFont.render(
                f"Press space to go to home screen", True, WHITE)
            surface.blit(text_surface, (Game.WIDTH / 5, Game.HEIGHT // 2))

    pygame.display.update()


def getCollition(platform, ball, counter):
    collisionTolerance = ball.BaseVelocity
    if ball.ball.left <= 0 or ball.ball.right >= Game.WIDTH:
        ball.angle = 180 - ball.angle - randint(-5, 5)
    if ball.ball.top <= 0:
        ball.angle *= -1
        ball.angle += randint(-5, 5)
    if platform.platform.colliderect(ball.ball):
        if abs(platform.platform.top - ball.ball.bottom) <= collisionTolerance * 2:
            ball.angle *= -1
            counter += 1
        if abs(platform.platform.right - ball.ball.left) <= collisionTolerance:
            ball.angle = 180 - ball.angle
        if abs(platform.platform.left - ball.ball.right) <= collisionTolerance:
            ball.angle = 180 - ball.angle
    if ball.ball.bottom >= Game.HEIGHT:
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
        platform.platform.x = xMouse - platform.WIDTH / 2


def gameOver():
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        return True
    return False


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
    drawing()
    Game.clock.tick(Game.FPS)
