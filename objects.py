DEFAULT_CONFIG = {"fill": "purple",
                  "side": 50,
                  "outline": "black",
                  "width": 1,
                  "cols":10,
                  "rows":10,
                  "enemy_size":8}

class Point():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def getX(self): return self.x

    def getY(self): return self.y


class Square():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.side = DEFAULT_CONFIG["side"]
        self.outline_color = DEFAULT_CONFIG["outline"]
        self.outline_width = DEFAULT_CONFIG["width"]
        self.fill_color = DEFAULT_CONFIG["fill"]

    def __repr__(self):
        return "Square(x: {}, y: {}, side: {}, fill_color: {} )".format(self.x, self.y, self.side, self.fill_color)

    def draw(self, canvas):
        pass


class Build(Square):
    def __init__(self, x, y, pathable=True):
        super().__init__(x, y)
        #self.can_be_path = pathable
        #self.fill_color = "green" if self.can_be_path else "red"
        self.fill_color = DEFAULT_CONFIG["fill"]

    def draw(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x + self.side, self.y + self.side, fill=self.fill_color,
                                       outline=self.outline_color, width=self.outline_width)

    def detect_cursor(self, point):
        return True if self.x <= point.x <= self.x + self.side and self.y <= point.y <= self.y + self.side else False


class Path(Square):
    def __init__(self, x, y, start=False, end=False):
        super().__init__(x, y)
        self.fill_color = "blue"
        self.start = start
        self.end = end

    def draw(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x + self.side, self.y + self.side, fill=self.fill_color,
                                       outline=self.outline_color, width=self.outline_width)

    def detect_cursor(self, point):
        return True if self.x <= point.x <= self.x + self.side and self.y <= point.y <= self.y + self.side else False


class Turret1(Square):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fill_color = "red"

    def draw(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x + self.side, self.y + self.side, fill=self.fill_color,
                                       outline=self.outline_color, width=self.outline_width)

    def detect_cursor(self, point):
        return True if self.x <= point.x <= self.x + self.side and self.y <= point.y <= self.y + self.side else False


class Enemy(Square):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = 100
        self.speed = 0.5
        self.vel_x = 1
        self.vel_y = 0
        self.passed = []
        self.fill_color = "orange"
        self.side = DEFAULT_CONFIG["enemy_size"]

    def draw(self, canvas):
        return canvas.create_oval(self.x, self.y, self.x + self.side, self.y + self.side, fill=self.fill_color,
                                  outline=self.outline_color, width=self.outline_width)

    def move(self):
        self.x += self.vel_x * self.speed
        self.y += self.vel_y * self.speed

    def set_dir(self, squares):
        closest_point = Point(10000, 10000)
        for s in squares:
            point = Point(s.x + s.side / 2, s.y + s.side / 2)
            print("--")
            print(point.x)
            print(point.y)
            print("--")
            if s not in self.passed and pow(pow(point.x - self.x, 2) + pow(point.y - self.y, 2), 1/2) < pow(pow(closest_point.x - self.x, 2) + pow(closest_point.y - self.y, 2), 1/2):
                closest_point = point

                print(closest_point.x)
                print(closest_point.y)
        #dX = point.x - self.x
        #dY = point.y - self.y

        #self.vel_x = (dX) / (dX) if abs(dX) > abs(point.y - self.y) else (dX) / (point.y - self.y)
        #self.vel_y = (point.y - self.y) / (point.y - self.y) if abs(point.y - self.y) > abs(point.x - self.x) else (point.y - self.y) / (point.x - self.x)

        dX = closest_point.x - self.x
        dY = closest_point.y - self.y

        if dX == 0:
            self.vel_x = 0
        else:
            self.vel_x = (closest_point.x - self.x) / (closest_point.x - self.x) if abs(closest_point.x - self.x) > abs(closest_point.y - self.y) else (closest_point.x - self.x) / (closest_point.y - self.y)

        if dY == 0:
            self.vel_y = 0
        else:
            self.vel_y = (closest_point.y - self.y) / (closest_point.y - self.y) if abs(closest_point.y - self.y) > abs(closest_point.x - self.x) else (closest_point.y - self.y) / (closest_point.x - self.x)






        print("Vel_x: {}, Vel_y: {}".format(self.vel_x, self.vel_y))


    def set_passed(self, squares):
        for s in squares:
            if abs(self.x + self.side / 2 - s.x < 5) and abs(self.y + self.side / 2 - s.y < 5):
                self.passed.append(s)
        print("penis")
