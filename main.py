import pygame
import pgzero
import pgzrun

from vector import Vector


class Paddle:
    def __init__(self, x, y):
        self.position = Vector(x, y)


WIDTH = 600
HEIGHT = 800


def draw():
    screen.fill("#123456")


def update(dt):
    pass


pgzrun.go()
