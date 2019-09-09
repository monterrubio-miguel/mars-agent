import random

from entities.drawable_entity import DrawableEntity
from utils import rect_in_world, rects_are_overlapping


class Rock(DrawableEntity):
    SIZE = 14
    COLOR = 'orange'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        top_left, bottom_right = self.get_bounds()
        canvas.create_oval(top_left.x,
                           top_left.y,
                           bottom_right.x,
                           bottom_right.y,
                           fill=self.COLOR)

    def has_room(self, world):
        """Checks whether self has room in world."""
        bounds = self.get_bounds()

        if not rect_in_world(bounds, world):
            return False

        for other in world.entities:
            # Rocks can be one on top of another, it doesn't matter.
            if isinstance(other, Rock):
                continue

            if rects_are_overlapping(bounds, other.get_bounds()):
                return False

        return True

    @staticmethod
    def generate_many(num, world):

        rocks = []
        condition = True
        while condition:
            x = random.randint(0, world.width-100)
            y = random.randint(0, world.height-100)

            rock = Rock(x, y)
            if rock.has_room(world):
                rocks.append(rock)

            rock = Rock(x + random.randint(-8,8), y + random.randint(-8,8))
            if rock.has_room(world):
                rocks.append(rock)

            rock = Rock(x + random.randint(-8,8), y + random.randint(-8,8))
            if rock.has_room(world):
                rocks.append(rock)

            rock = Rock(x + random.randint(-8,8), y + random.randint(-8,8))
            if rock.has_room(world):
                rocks.append(rock)

            if len(rocks) < num:
                condition = True
            else:
                condition = False
                
        return rocks
