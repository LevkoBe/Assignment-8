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
                game_is_running = False
            self.position.y = HEIGHT - R - 1

        if self.position.y >= 385 and paddle.position - R <= self.position.x <= paddle.position + W + R:
            self.velocity.y = -VER_SPEED
            self.velocity.x += paddle.velocity

    def change_of_direction(self, obstacle):
        change_of_x = self.position.x - obstacle.position.x
        change_of_y = self.position.y - obstacle.position.y
        self.velocity = Vector(change_of_x, change_of_y).normalized() * 30


class Heart:
    def __init__(self, x):
        self.actor = Actor("heart.png", center=(x, 20))

    def draw(self):
        self.actor.draw()


class Obstacle:
    def __init__(self, x, y, color):
        self.position = Vector(x, y)
        self.color = color

    def draw(self):
        screen.draw.filled_circle((self.position.x, self.position.y), R, self.color)

    def hit(self):
        if (self.position - ball.position).magnitude() <= 2 * R:
            return True


class BonusLife:
    def __init__(self):
        self.actor = Actor("heart.png", center=(random.randint(0, WIDTH), 0))

    def draw(self):
        self.actor.draw()

    def update(self):
        self.actor.y += 1
        self.hit()

    def hit(self):
        global bonus_life
        if self.actor.y >= 385 and paddle.position <= self.actor.x <= paddle.position + W:
            self.actor.x = random.randint(0, WIDTH)
            self.actor.y = 0
            hearts.append(Heart((len(hearts) + 1) * 20))
            bonus_life = False
        if self.actor.y >= 400:
            bonus_life = False
            self.actor.y = 0


TEXT = 'The game is over'
WIDTH = 600  # 600
HEIGHT = 400  # 800
W = 100  # 200
H = 10  # 20
R = 7
VER_SPEED = 30

obstacles = []
for a in range(57):
    x = (a % 19 + 1) * 30
    y = (a // 19 + 1) * 30
    obstacles.append(Obstacle(x, y, (0, 255, 255)))

paddle = Paddle((WIDTH - W) / 2, 0)
ball = Ball(Vector(WIDTH / 2, HEIGHT / 2))

hearts = []
for x in range(3):
    hearts.append(Heart((x + 1) * 20))
game_is_running = True

ball.x = 3
ball.y = 30

bonus_life = False
bonuslife0 = BonusLife()


def draw():
    screen.clear()
    screen.fill("#123456")
    if game_is_running:
        ball.draw()
        for heart in hearts:
            heart.draw()
        for obstacle in obstacles:
            obstacle.draw()
    else:
        screen.draw.text(TEXT, center=(300, 200), fontsize=60, color=(255, 136, 0), shadow=(2, 2))
    paddle.draw()

    if bonus_life:
        bonuslife0.draw()


def update(dt):
    global bonus_life
    ball.move(dt)
    if len(obstacles) == 0:
        global game_is_running, TEXT
        TEXT = 'You won'
        game_is_running = False
    else:
        for obstacle in obstacles:
            if obstacle.hit():
                ball.change_of_direction(obstacle)
                obstacles.remove(obstacle)
    if random.random() > 0.8 and not bonus_life:
        bonus_life = True
    else:
        bonuslife0.update()


def on_mouse_move(pos):
    paddle.move(pos)


def on_key_down(key):
    if key == keys.MINUS:
        if len(obstacles) != 0:
            obstacles.remove(obstacles[len(obstacles) - 1])


pgzrun.go()
