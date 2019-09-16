import random

from entities.drawable_entity import DrawableEntity
from entities.morona import Morona
from entities.rock import Rock
from utils import rect_in_world, rects_are_overlapping, normalize


class Explorer(DrawableEntity):
    SIZE = 10
    MAX_VELOCITY = 1.3
    PICKUP_REACH = .1
    SENSOR_RANGE = 30
    SENSE_DELAY = 100
    COLOR = 'blue'
    HAS_ROCK_COLOR = 'yellow'
    SENSOR_COLOR = 'yellow'

    def __init__(self, x, y, world, isCoop):
        self.x = x
        self.y = y
        self.world = world
        self.dx, self.dy = self._get_new_direction()
        self.ticks = 0
        self.has_rock = False
        self.tempdx, self.tempdy = self._get_new_direction()
        self.isCoop = isCoop
        print(self.isCoop)

    def draw(self, canvas):
        # Helper is the sensor. Detects objects when within range specified above
        helper = Explorer(self.x, self.y, self.world, self.isCoop)
        helper.SIZE = 2 * self.SENSOR_RANGE + self.SIZE

        #Draws sensor range as a circle
        top_left, bottom_right = helper.get_bounds()
        canvas.create_oval(top_left.x,
                           top_left.y,
                           bottom_right.x,
                           bottom_right.y,
                           outline=self.SENSOR_COLOR)

        # Draws Explorer as a square
        top_left, bottom_right = self.get_bounds()
        canvas.create_rectangle(top_left.x,
                                top_left.y,
                                bottom_right.x,
                                bottom_right.y,
                                fill=self.HAS_ROCK_COLOR if self.has_rock else self.COLOR)

    def tick(self):
        self._tick()
        self.ticks += 1

    #function runs each tick
    def _tick(self):
        #--------------------------------
        #CAPA 1
        #--------------------------------
        #avoids obstacle if they are in sensor range
        obstacle = self._obstacle_range()
        if obstacle:

            self.tempdx, self.tempdy = normalize(obstacle.x - self.x,
                                                 obstacle.y - self.y)

            if self.ticks % 5 == 0:
                self.dx = self.tempdy
                self.dy = -self.tempdx
            
            if self.ticks % 10 == 0 and self.has_rock and self.isCoop == True:
                morona = Morona(self.x, 
                                self.y, 
                                self.dx, 
                                self.dy)
                self.world.add_entity(morona)

            self._move()
            return

        
        if self.has_rock:
            #--------------------------------
            #CAPA 2
            #--------------------------------
            # If at base, drop rock
            if self._drop_available():
                self.has_rock = False
                self.world.rock_collected()

                if self.isCoop == True:
                    #leaves crumb at base
                    morona = Morona(self.x, 
                                    self.y, 
                                    self.dx, 
                                    self.dy)
                    self.world.add_entity(morona)
                return

            #--------------------------------
            #CAPA 3
            #--------------------------------
            # If with rock and not at base, move towards base
            self.dx, self.dy = normalize(self.world.mars_base.x - self.x,
                                         self.world.mars_base.y - self.y)

            # Drop crumbs every 15 ticks (does not drop crumb in tick "0")
            if self.ticks % 10 == 0 and self.ticks > 0 and self.isCoop == True:
                morona = Morona(self.x, 
                                self.y, 
                                self.dx, 
                                self.dy)
                self.world.add_entity(morona)
                
        else:
            #--------------------------------
            #CAPA 4
            #--------------------------------
            # Pick up.
            rock = self._rock_available()
            if rock:
                self.has_rock = True
                self.world.remove_entity(rock)
                return

            # Head towards rock if detected
            rock = self._sense_rock()
            if rock:
                self.dx, self.dy = normalize(rock.x - self.x, rock.y - self.y)


            #--------------------------------
            #CAPA 5
            #--------------------------------
            # Pick up crumb and continue moving
            morona = self._morona_available()
            if morona:
                self.dx = morona.dx * -1
                self.dy = morona.dy * -1
                self.world.remove_entity(morona)

        #--------------------------------
        #CAPA 6
        #--------------------------------
        # Move randomly. Change direction if unable to move
        if self.ticks % 200 == 0 and self._morona_range() == 0:
            self.dx, self.dy = self._get_new_direction()

        if not self._can_move():
            self.dx, self.dy = self._get_new_direction()
            
        self._move()

    #enables movement
    def _move(self):
        self.x += self.dx
        self.y += self.dy

    #obtains new random direction
    def _get_new_direction(self):
        dx = random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY)
        dy = random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY)
        return normalize(dx, dy)

    #checks if explorer is stuck
    def _can_move(self):
        new_self = Explorer(self.x + self.dx,
                            self.y + self.dy,
                            self.world,
                            self.isCoop)
        bounds = new_self.get_bounds()

        if not rect_in_world(bounds, new_self.world):
            return False

        for other in new_self.world.entities:
            # Allow collisions with other explorers.
            if isinstance(other, Explorer):
                continue

            if isinstance(other, Morona):
                continue

            if isinstance(other, Rock):
                continue

            if rects_are_overlapping(bounds, other.get_bounds()):
                return False
        return True

    #check if explorer can pick up rock
    def _rock_available(self):
        for rock in self.world.rocks:
            if rects_are_overlapping(self.get_bounds(),
                                     rock.get_bounds(),
                                     self.PICKUP_REACH):
                return rock
        return None

    #check if explorer can pick up crumb
    def _morona_available(self):
        for morona in self.world.moronas:
            if rects_are_overlapping(self.get_bounds(),
                                     morona.get_bounds(),
                                     self.PICKUP_REACH):
                return morona
        return None

    #check if crumb is in range
    def _morona_range(self):
        for morona in self.world.moronas:
            if rects_are_overlapping(self.get_bounds(),
                                     morona.get_bounds(),
                                     self.SENSOR_RANGE):
                return morona
        return None

    #check if obstacle is close
    def _obstacle_range(self):
        if self.has_rock:
            obstacle_range = 10
        else:
            obstacle_range = 1

        for obstacle in self.world.obstacles:
            if rects_are_overlapping(self.get_bounds(),
                                     obstacle.get_bounds(),
                                     obstacle_range):
                return obstacle
        return None

    #checks if rock is in range of sensor
    def _sense_rock(self):
        # Wait a bit so that the explorers spread out.
        if self.ticks < self.SENSE_DELAY:
            return None

        for rock in self.world.rocks:
            if rects_are_overlapping(self.get_bounds(),
                                     rock.get_bounds(),
                                     self.SENSOR_RANGE):
                return rock

        return None

    #checks if base is in range to drop off rock
    def _drop_available(self):
        if rects_are_overlapping(self.get_bounds(),
                                 self.world.mars_base.get_bounds(),
                                 self.PICKUP_REACH):
            return True
        return False
