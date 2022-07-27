import turtle
import numpy as np

turtle.tracer(0, 0)

g = 9.81
x = 0
y = 0
vx = 1
vy = 50
p = 0.5
i = 0.1
d = 0.2
dt = 0.001
scale = 1
t = 0

wn = turtle.Screen()
wn.setup(0.5,0.5)


axis_list = turtle.Turtle(), turtle.Turtle(), turtle.Turtle(), turtle.Turtle()
axis_number = 0
for axis in axis_list:
    axis.up()
    axis.goto(30 * np.cos(np.pi/2 * axis_number), 30 * np.sin(np.pi/2 * axis_number))
    axis.left(180 + axis_number*90)
    axis_number += 1

test = turtle.Turtle()
test.shape("square")
test.goto(x, y)
test.vx = vx
test.vy = vy

dt = dt * scale

turtle.tracer(1, 1)

test2 = turtle.Turtle()
test2.goto(0, 127)
print(dt)
while True:
    test.goto(test.xcor() + vx * dt, test.ycor() + vy * dt)
    vy -= g * dt
    # turtle.update()