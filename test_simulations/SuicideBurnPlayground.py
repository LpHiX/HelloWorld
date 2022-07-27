from vpython import *
import numpy as np

G = 9.81
vy = -10
vx = 0
y = 100

m0 = 500
fuel = 400
F = 10000
I = 10


# scene = canvas(width=2030,height=1120)
scene = canvas(width=900,height=1000)

plat = box(size=vec(100, 0.1, 100), pos=vec(0, -0.05, 0), opacity=1, color=vec(0.5, 1, 0.5))
test = box(size=vec(15, 0.1, -15), pos=vec(0, y, 0))
label0 = label(pos=vec(25,-5,0))
label1 = label(pos=vec(25,-10,0))
label2 = label(pos=vec(25,-15,0))
test.vel = vec(vx, vy, 0)
velocity_arrow = arrow(pos=vec(0, y, 0), axis=vec(0, vy, 0), shaftwidth=1)
gravity_arrow = arrow(pos=vec(5, y, 0), axis=vec(0, -G, 0), shaftwidth=1)
thrust_arrow = arrow(pos=vec(5, y, 0), axis=vec(0, 0, 0), shaftwidth=1)
m1 = m0
a = F / m1
dt = 0.0001
t = 0
time_burnt = 0

scene.follow(test)

acceleration = (F / m1) - G
start_burn_height = -(np.sign(test.vel.y) * test.vel.y ** 2) / (2 * acceleration)


def throttle():
    global m1
    global time_burnt
    if m1 > m0-fuel:
        mdot = F / (I * G)
        test.vel.y += F*dt / m1
        m1 -= mdot * dt
        time_burnt += dt
print(m1)

while test.pos.y > 0:
    burning = False
    acceleration = (F / m1) - G
    start_burn_height = -(np.sign(test.vel.y) * test.vel.y**2) / (2 * acceleration)

    k = keysdown()
    if 'shift' in k:
        burning = True
        test.color = vec(1, 0.5, 1)
    else:
        test.color = vec(1, 1, 1)

    if test.pos.y < start_burn_height:
        burning = True
        test.color = vec(1, 1, 0)

    if burning:
        throttle()
        if m1 > m0 - fuel:
            thrust_arrow.axis = vec(0, F/m1, 0)
    else:
        thrust_arrow.axis = vec(0, 0.1, 0)

    label0.text = "Total time", '%0.3f'%t, "Time burning:", '%0.3f'%time_burnt
    label1.text = "Y:", '%0.3f'%test.pos.y, "VY:", '%0.3f'%test.vel.y, "M0", m0, "Mass", '%0.3f'%m1
    label2.text = "Burn starts at", '%0.3f'%start_burn_height, "Net Acceleration", '%0.3f'%acceleration

    velocity_arrow.pos = test.pos
    velocity_arrow.axis = test.vel

    gravity_arrow.pos = test.pos - vec(5, 0, 0)
    thrust_arrow.pos = test.pos - vec(5, 0, 0)

    rate(10000)
    test.vel.y -= G * dt
    test.pos += test.vel * dt
    t += dt

if test.vel.y > 0 or test.vel.mag > 1:
    test.color = (vec(1, 0, 0))
else:
    test.color = (vec(0, 1, 0))

print("Time:",'%0.3f'%t)
print("Y:", '%0.3f'%test.pos.y)
print("Velocity:", '%0.3f'%test.vel.y)
print("Time Burnt:", '%0.3f'%time_burnt)
print("Final Mass:", '%0.3f'%m1)