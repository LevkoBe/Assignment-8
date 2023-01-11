import pgzrun
import random
from pgzero.actor import Actor

from vector import Vector


class Paddle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def draw(self):
        screen.draw.filled_rect(Rect(self.position, HEIGHT - H, W, H), "#08a704")

    def move(self, pos):
        p = pos[0] - W / 2
        if 0 < p < WIDTH - W:
            self.velocity = p - self.position
            self.position = p
        else:
            self.velocity = 0


class Ball:
    def __init__(self, position: Vector):
        self.position = position
        self.velocity = Vector(random.randint(-30, 30), VER_SPEED)

    def draw(self):
        screen.draw.filled_circle((self.position.x, self.position.y), R, "#ff7c00")

    def move(self, dt):
        self.hit()
        if self.velocity.x > VER_SPEED:
            self.velocity.x = VER_SPEED
        self.position += self.velocity * dt * 10

    def hit(self):

        if self.position.x <= R:
            self.velocity.x = abs(self.velocity.x)

        elif self.position.x >= WIDTH - R:
            self.velocity.x = -abs(self.velocity.x)

        if self.position.y <= R:
            self.velocity.y = VER_SPEED

        elif self.position.y >= HEIGHT - R:
            self.velocity = Vector(0, 0)

        if self.position.y >= 385 and paddle.position - R <= self.position.x <= paddle.position + W + R:
            self.velocity.y = -VER_SPEED
            self.velocity.x += paddle.velocity

class Heart:
    def __init__(self, x):
        self.actor = Actor("heart.png", center=(x, 20))
        
    def draw(self):
        self.actor.draw()

WIDTH = 600  # 600
HEIGHT = 400  # 800
W = 100  # 200
H = 10  # 20
R = 7
VER_SPEED = 30

paddle = Paddle((WIDTH - W) / 2, 0)
ball = Ball(Vector(WIDTH / 2, HEIGHT / 2))
heart = Heart(20)
heart1 = Heart(40)
heart2 = Heart(60)

ball.x = 3
ball.y = 30


def draw():
    screen.clear()
    screen.fill("#123456")
    paddle.draw()
    ball.draw()
    heart.draw()
    heart1.draw()
    heart2.draw()


def update(dt):
    ball.move(dt)


def on_mouse_move(pos):
    paddle.move(pos)


pgzrun.go()
