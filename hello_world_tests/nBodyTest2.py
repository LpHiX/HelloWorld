from vpython import *

canvas(width=1950, height=1050)

ball = sphere(pos=vector(0, 10, 0), radius=1, color=color.green)
floor = box(pos=vector(0, 0, 0), size=vector(100, .1, 100))
t = 0
dt = 0.001
gravity = -10
ball.velocity = vector(0, 0, 0)

a = 0

while True:
    k = keysdown()
    if 'up' in k: ball.velocity.y += 0.1
    if 'down' in k: ball.velocity.y -= 0.1
    if 'right' in k: ball.velocity.x += 0.1
    if 'left' in k: ball.velocity.x -= 0.1

    rate(1000)
    ball.velocity.y += gravity * dt
    ball.pos = ball.pos + ball.velocity * dt
    t = t + dt

    if ball.pos.y - 0.5 < floor.pos.y:
        ball.velocity.y = -ball.velocity.y
