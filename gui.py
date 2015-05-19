from Tkinter import Tk, Canvas

from drawable_entity import DrawableEntity


class GUI(object):
    def __init__(self, width, height):
        self.ticks = 0
        self.width = width
        self.height = height
        self.entities = []

        self.root = Tk()
        self.root.title("Mars Explorer")
        window_x, window_y = self._compute_window_coords()
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height,
                                            window_x, window_y))

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.after(1, self._tick)

    def start(self):
        self.root.mainloop()

    def add_entity(self, entity):
        assert isinstance(entity, DrawableEntity)
        self.entities.append(entity)

    def _tick(self):
        self._draw()

        self.ticks += 1
        self.canvas.after(1, self._tick)

    def _draw(self):
        self.canvas.delete('all')

        for entity in self.entities:
            entity.draw(self.canvas)

        self.canvas.create_text(self.width - 20, 10, text=str(self.ticks))

    def _compute_window_coords(self):
        # http://stackoverflow.com/a/14912644/742501
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_x = screen_width / 2 - self.width / 2
        window_y = screen_height / 2 - self.height / 2
        return window_x, window_y