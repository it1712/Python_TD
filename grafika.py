# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill": "red",
                  "size": "10",
                  "outline": "black",
                  "width": "10", }

import math

class Point():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def draw(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x + 10, self.y + 10, fill=DEFAULT_CONFIG['fill'])

    def clone(self):
        other = Point(self.x, self.y)
        other.config = self.config.copy()
        return other

    def getX(self): return self.x

    def getY(self): return self.y


class Square():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = DEFAULT_CONFIG["size"]
        self.height = DEFAULT_CONFIG["size"]
        self.outline_color = DEFAULT_CONFIG["outline"]
        self.outline_width = DEFAULT_CONFIG["width"]
        self.fill_color = DEFAULT_CONFIG["fill"]

    def __repr__(self):
        return "Square(x: {}, y: {}, width: {}, height: {}, fill_color: {} )".format(self.x, self.y, self.width,
                                                                                    self.height, self.fill_color)

    def draw(self, canvas):
        pass



class Rectangle(Square):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fill_color = DEFAULT_CONFIG["fill"]

    def __repr__(self):
        return "Rectangle(x: {}, y: {}, width: {}, height: {}, fill_color: {}, width:{} )".format(self.x, self.y,
                                                                                                  self.width, self.height,
                                                                                                  self.fill_color,
                                                                                                  width=self.outline_width)

    def draw(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.fill_color,
                                       outline=self.outline_color, width=self.outline_width)

    def detect_cursor(self, point):
        return True if self.x <= point.x <= self.x + self.width and self.y <= point.y <= self.y + self.height else False


class Oval(Square):
    def __repr__(self):
        return "Oval(x: {}, y: {}, width: {}, height: {}, fill_color: {}, width:{} )".format(self.x, self.y, self.width,
                                                                                             self.height,
                                                                                             self.fill_color,
                                                                                             width=self.outline_width)

    def draw(self, canvas):
        return canvas.create_oval(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.fill_color,
                                  outline=self.outline_color, width=self.outline_width)

    def detect_cursor(self, point):
        e = math.sqrt(math.pow(self.width / 2, 2) - math.pow(self.height / 2, 2))

        return True if self.x <= point.x <= self.x + self.width and self.y <= point.y <= self.y + self.height else False

