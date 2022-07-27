class Balls:
    dt = 1

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def iterate(self):
        self.x = self.x + self.dx * self.dt

    def print(self):
        print(str(self.x) + " " + str(self.y))


ball1 = Balls(0, 0, 5, 10)
ball2 = Balls(10000, -100, -5, 10)
for x in range(0,100):
    ball1.iterate()
    ball2.iterate()

ball1.print()
ball2.print()