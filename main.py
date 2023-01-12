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
            global game_is_running
            self.velocity = Vector(0, 0)
            if len(hearts) > 0:
                hearts.remove(hearts[len(hearts) - 1])
            if len(hearts) == 0:
                print("Game over!")
                game_is_running = False
            self.position.y = HEIGHT - R - 1

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
hearts = []
for x in range(3):
    hearts.append(Heart((x + 1) * 20))
game_is_running = True

ball.x = 3
ball.y = 30


def draw():
    screen.clear()
    screen.fill("#123456")
    if game_is_running:
        ball.draw()
        for heart in hearts:
            heart.draw()
    else:
        screen.draw.text(f"The game is over!", center=(300, 200), fontsize = 60, color=(255, 136, 0), shadow=(2,2))
    paddle.draw()


def update(dt):
    ball.move(dt)


def on_mouse_move(pos):
    paddle.move(pos)


pgzrun.go()
