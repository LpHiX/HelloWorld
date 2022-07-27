import turtle
import math
import time
import random

turtle.tracer(0, 0)
turtle.delay(0)

gravity = 1

wn = turtle.Screen()
wn.screensize(3000,3000)
wn.setup(1.0,1.0)

balls = []
particles = []

axis = turtle.Turtle()
axis.dot()
axis.hideturtle()


def createBall(mass, radius, x, y, dx, dy, color, main):
    ball = turtle.Turtle()
    ball.up()
    ball.mass = mass
    ball.radius = radius
    ball.turtlesize(radius/10)
    ball.shape("circle")
    ball.goto(x, y)
    ball.dx = dx
    ball.dy = dy
    ball.color(color)
    if main:
        balls.append(ball)
        #ball.down()
    else:
        particles.append(ball)


def g_force(first, second):
    distance = math.sqrt((second.ycor() - first.ycor()) ** 2 + (second.xcor() - first.xcor()) ** 2)
    force = gravity * first.mass * second.mass / distance**2
    return force

createBall(1e2, 10, 0, 0, 0, 0, "green", True)
#createBall(40, 10, -300, 0, 0, -6, "green", True)
#createBall(-1000, 15, 450, 0, 0, 4, "orange", True)
#createBall(-1000, 15, -450, 0, 0, -4, "orange", True)
createBall(1e1, 10, -100, 0, 0, 1, "red", True)

#for x in range(20):
#    createBall(1, 3, random.random()*25-10, random.random()*25-500, random.random() - 5.5, random.random() -1, "blue", False)
#    createBall(random.random()*1000, 10, random.random() * 1200 - 600, random.random() * 1200 - 600, random.random() * 10 - 5, random.random() * 10 - 5, "blue", True)
time.sleep(2)
duration = 0
while True:
    for ball in balls:
        for ball2 in balls:
            if ball2 != ball:
                angle = math.atan2(ball.ycor() - ball2.ycor(), ball.xcor() - ball2.xcor())
                ball.dx -= g_force(ball, ball2) / ball.mass * math.cos(angle)
                ball.dy -= g_force(ball, ball2) / ball.mass * math.sin(angle)
        ball.goto(ball.xcor() + ball.dx, ball.ycor() + ball.dy)
    for ball in particles:
        for ball2 in balls:
            angle = math.atan2(ball.ycor() - ball2.ycor(), ball.xcor() - ball2.xcor())
            ball.dx -= g_force(ball, ball2) / ball.mass * math.cos(angle)
            ball.dy -= g_force(ball, ball2) / ball.mass * math.sin(angle)
        ball.goto(ball.xcor() + ball.dx, ball.ycor() + ball.dy)
        print(ball.x, ball.y)
        print(ball.dx, ball.dy)
    duration += 1
    if duration % 1 == 0:
        turtle.update()
    time.sleep(0.01)

