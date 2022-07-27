import turtle
import time

# Global Parameters
t = 0
dt = 0.001

# -----------------

turtle.tracer(0, 0)


class Simulator:
    def __init__(self):
        self.testObject = Rocket()
        self.screen = turtle.Screen()
        self.screen.setup(1200, 1000)
        self.sim = True

    def create_axis(self):
        x_axis = turtle.Turtle()
        x_axis.pu()
        x_axis.goto(-500, 0)
        for x_axi in range(-5, 6):
            x_axis.dot()
            x_axis.goto(x_axi * 100, 0)
        x_axis.hideturtle()

    def cycle(self):
        while self.sim:
            global t
            turtle.update()
            self.testObject.Rocket.goto(t * 100, 0)
            if self.testObject.Rocket.xcor() > 1200: self.testObject.Rocket.goto(-1200, 0)
            t += dt
            print(t, round(time.time()*1000))


class Rocket:
    def __init__(self):
        self.Rocket = turtle.Turtle()
        self.Rocket.pu()


def main():
    sim = Simulator()
    sim.create_axis()
    turtle.tracer(1, 1)

    sim.cycle()


main()
