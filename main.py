import pgzrun

from vector import Vector


class Paddle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def draw(self):
        x = self.position
        screen.draw.filled_rect(Rect(x, HEIGHT - H, W, H), (255, 153, 51))

    def move(self, pos):
        p = pos[0] - W / 2
        if 0 < p < WIDTH - W:
            self.velocity = p - self.position
            self.position = p
        else:
            self.velocity = 0


WIDTH = 600
HEIGHT = 800
W = 200
H = 20
paddle = Paddle((WIDTH - W) / 2, 0)


def draw():
    screen.clear()
    screen.fill("#123456")
    paddle.draw()


def update(dt):
    pass


def on_mouse_move(pos):
    paddle.move(pos)


pgzrun.go()
