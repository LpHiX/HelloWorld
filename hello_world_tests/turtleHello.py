import turtle
import math
import time

turtle.tracer(0, 0)
turtle.delay(0)


#-----------VARIABLES
gravity = 1
speed = 1
density = 0.0001
ball_number = 10
starting_x = -200
separation = 100

wn = turtle.Screen()
wn.screensize(10000, 10000)
origin = turtle.Turtle()
wn.setup(1.0,1.0)

origin.radius = 100
origin.mass = density * (4 / 3) * math.pi * origin.radius**3

print("mass:")
print(origin.mass)

origin.penup()
origin.shape("circle")
origin.color("orange")
origin.goto(0, -origin.radius)
origin.pendown()
origin.circle(origin.radius)
origin.penup()
origin.goto(0, 0)


balls = []

for _ in range(ball_number):
    balls.append(turtle.Turtle())

ballNumber = 0


def circ_v(d):
    if d > origin.radius:
        velocity = math.sqrt(gravity * origin.mass / d)
        print("out")
        print(d)
        print(velocity)
    else:
        velocity = d * math.sqrt(gravity * density * (4 / 3) * math.pi)
        print("in")
    return 2


def accel_g(d):
    if d > origin.radius:
        acceleration = (gravity * origin.mass / d**2)
    else:
        acceleration = gravity * density * (4 / 3) * math.pi * d
    return acceleration


for ball in balls:
    ball.shape("circle")
    ball.color("green")
    ball.turtlesize(0.3,0.3)
    ball.speed(0)
    ball.penup()
    ball.goto(starting_x - separation * ballNumber, 0)
    #ball.pendown()
    ball.dy = circ_v(abs(starting_x - separation * ballNumber))
    ball.dy = 0.1
    ball.dx = 0
    ball.mass = 100
    ball.totalDistance = 0
    ball.time = 0
    ballNumber += 1
    #ball.ht()


while True:
    for ball in balls:
        ball.angle = math.atan2(ball.ycor() - origin.ycor(), ball.xcor() - origin.xcor())
        ball.d = math.sqrt((origin.ycor()-ball.ycor()) ** 2 + (origin.xcor()-ball.xcor()) ** 2)
        ball.dy += -(accel_g(ball.d) * math.sin(ball.angle))
        ball.dx += -(accel_g(ball.d) * math.cos(ball.angle))
        ball.goto(ball.xcor() + ball.dx, ball.ycor() + ball.dy)
    turtle.update()
    time.sleep(.0000001)