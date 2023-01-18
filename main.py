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

    def change_size(self):
        global W, bonus
        W = 150
        bonus = False
        clock.schedule_unique(self.reset_size, 15)

    def reset_size(self):
        global W
        W = 100


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
    def __init__(self, x, y, level):
        self.position = Vector(x, y)
        self.level = level
        self.color = (85 * level, 255, 80 * level)

    def draw(self):
        screen.draw.filled_circle((self.position.x, self.position.y), R, self.color)

    def hit(self, obstacle):
        if (self.position - ball.position).magnitude() <= 2 * R:
            ball.change_of_direction(obstacle)
            obstacle.change_level(obstacle)

    def change_level(self, obstacle):
        if self.level > 1:
            self.level -= 1
            self.color = (85 * self.level, 255, 80 * self.level)
        else:
            obstacles.remove(obstacle)


class SquareObstacle:
    def __init__(self, x, y, level):
        self.position = Vector(x, y)
        self.level = level
        self.color = (85 * level, 80 * level, 255)

    def draw(self):
        screen.draw.filled_rect(Rect((self.position.x - R, self.position.y - R),
                                     (2 * R, 2 * R)), self.color)

    def hit(self, obstacle):
        if self.position.x - R <= ball.position.x <= self.position.x + R and \
                self.position.y - R - R <= ball.position.y <= self.position.y + R + R:
            ball.velocity = Vector(ball.velocity.x, -ball.velocity.y)
            self.change_level(obstacle)
        elif self.position.y - R <= ball.position.y <= self.position.y + R and \
                self.position.x - R - R <= ball.position.x <= self.position.x + R + R:
            ball.velocity = Vector(-ball.velocity.x, ball.velocity.y)
            self.change_level(obstacle)
        elif (self.position - ball.position).magnitude() <= 17 and \
                (self.position.x - R >= ball.position.x or ball.position.x >= self.position.x + R) and \
                (self.position.y - R >= ball.position.y or ball.position.y >= self.position.y + R):
            ball.change_of_direction(obstacle)
            self.change_level(obstacle)

    def change_level(self, obstacle):
        if self.level > 1:
            self.level -= 1
            self.color = (85 * self.level, 255, 80 * self.level)
        else:
            obstacles.remove(obstacle)


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
            self.actor.x = random.randint(0, WIDTH)
            self.actor.y = 0


class SpecialBonus:
    def __init__(self):
        self.actor = Actor("bonus.png", center=(random.randint(0, WIDTH), 0))
        self.x = 0

    def draw(self):
        self.actor.draw()

    def update(self):
        self.actor.y += 1
        self.x += 1
        if self.x == 100:
            self.x = -100
        if self.x != 0:
            self.actor.x += self.x / abs(self.x)
        self.hit()

    def hit(self):
        global bonus
        if self.actor.y >= 400:
            self.actor.x = random.randint(0, WIDTH)
            self.actor.y = 0
            bonus = False
        elif self.actor.y >= 385 and paddle.position <= self.actor.x <= paddle.position + W:
            self.actor.x = random.randint(0, WIDTH)
            self.actor.y = 0
            paddle.change_size()


TEXT = 'Choose level 1/2 '
WIDTH = 600  # 600
HEIGHT = 400  # 800
W = 100  # 200
H = 10  # 20
R = 7
VER_SPEED = 30

paddle = Paddle((WIDTH - W) / 2, 0)
ball = Ball(Vector(WIDTH / 2, HEIGHT / 2))

obstacles = []
hearts = []
for x in range(3):
    hearts.append(Heart((x + 1) * 20))
game_is_running = False

ball.x = 3
ball.y = 30

bonus = False
bonus_life = False
bonus_life_0 = BonusLife()
s_bonus = SpecialBonus()


def start_g(figure):
    global obstacles, hearts
    obstacles = []
    hearts = []
    for x_h in range(3):
        hearts.append(Heart((x_h + 1) * 20))
    for a in range(57):
        x_o = (a % 19 + 1) * 30
        y_o = (a // 19 + 1) * 30
        if figure == "circle":
            obstacles.append(Obstacle(x_o, y_o, random.randint(1, 3)))
        else:
            obstacles.append(SquareObstacle(x_o, y_o, random.randint(1, 3)))


def draw():
    screen.clear()
    screen.fill("#123456")
    if game_is_running:
        ball.draw()
        for heart in hearts:
            heart.draw()
        for obstacle in obstacles:
            obstacle.draw()
        if bonus:
            s_bonus.draw()
        if bonus_life:
            bonus_life_0.draw()
        paddle.draw()
    else:
        screen.draw.text(TEXT, center=(300, 200), fontsize=60, color=(255, 136, 0), shadow=(2, 2))


def update(dt):
    global bonus_life, bonus, game_is_running, TEXT
    ball.move(dt)
    if len(obstacles) == 0 and game_is_running:
        TEXT = 'You won'
        game_is_running = False
    else:
        for obstacle in obstacles:
            obstacle.hit(obstacle)
    if random.random() > 0.999 and not bonus_life:
        bonus_life = True
    else:
        bonus_life_0.update()
    if random.random() > 0.999 and not bonus:
        bonus = True
    if len(hearts) == 0:
        TEXT = 'The game is over'
    else:
        s_bonus.update()


def on_mouse_move(pos):
    paddle.move(pos)


def on_key_down(key):
    global game_is_running
    if key == keys.MINUS:
        if len(obstacles) != 0:
            obstacles.remove(obstacles[len(obstacles) - 1])
    if key == keys.DELETE:
        for x in range(57):
            if len(obstacles) != 3:
                obstacles.remove(obstacles[len(obstacles) - 1])
    elif key == keys.K_1:
        start_g("circle")
        game_is_running = True
    elif key == keys.K_2:
        start_g("square")
        game_is_running = True


pgzrun.go()
