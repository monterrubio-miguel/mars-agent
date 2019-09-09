import random

from entities.drawable_entity import DrawableEntity
from utils import rect_in_world, rects_are_overlapping, normalize


class Morona(DrawableEntity):
    SIZE= 5
    COLOR= 'green'

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.ticks = 0

    def draw(self, canvas):
        top_left, bottom_right = self.get_bounds()
        canvas.create_rectangle(top_left.x,
                                top_left.y,
                                bottom_right.x,
                                bottom_right.y,
                                fill=self.COLOR)
