import pgzrun
import random

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



class Ball:
    def __init__(self,position:Vector): 
        self.position = position
        self.velocity = Vector(random.randint(-20 ,20),random.randint(10 ,60))

    def draw(self):
        screen.draw.filled_circle((self.position.x, self.position.y), 5, 'green')

    def move(self, dt):
        self.position += self.velocity * dt
    
    



WIDTH = 600 # 600
HEIGHT = 400 #800
W = 100 # 200
H =10 # 20

paddle = Paddle((WIDTH - W) / 2, 0)
ball = Ball(Vector(WIDTH / 2, HEIGHT /2))



ball.x = 3
ball.y = 30

def draw():
    screen.clear()
    screen.fill("#123456")
    paddle.draw()
    ball.draw()
    


def update(dt):
    ball.move(dt)


def on_mouse_move(pos):
    paddle.move(pos)


pgzrun.go()
