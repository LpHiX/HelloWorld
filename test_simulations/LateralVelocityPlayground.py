from vpython import *

# import numpy as np

f1 = gcurve(color=color.cyan)  # a graphics curve
# scene = canvas(width=2030,height=1120)
# scene = canvas(width=900,height=700)
scene = canvas(width=500, height=500)

vx = 0
rx = 0

m0 = 500
fuel = 400
F = 10000
Isp = 100

starting_angle = 0
tar_angle = 0
torque = 1000

animation_speed = 1

background = box(size=vec(20, 20, 0.1), pos=vec(0, 0, 0), opacity=.8, color=vec(1, 1, 0.5))
test = pyramid(pos=vec(0, 0, 1), size=vec(3, 5, 1), make_trail=True, color=vec(0, 0, 0), trail_color=vec(0, 0.5, 0))
tar_angle_display = sphere(pos=vec(6 * cos(tar_angle), 6 * sin(tar_angle), 0), radius=0.2, color=vec(0, 0, 0))
test.vel = vec(vx, 0, 0)
test.rot_v = rx

# Setting up variables -----------------------

dt = 0.001
t = 0
turn_t = 0
stop = False
test.angle = starting_angle

space = "                                        "

test.rotate(starting_angle, vec(0, 0, 1))


# Widget Creation --------------------


def angle_slider(angle_value):
    global tar_angle
    global starting_angle
    global turn_t
    angle_label.text = str(angle_value.value)
    tar_angle = angle_value.value
    starting_angle = test.angle % (2 * pi)
    turn_t = 0
    tar_angle_display.pos = vec(6 * cos(tar_angle), 6 * sin(tar_angle), 0)


slider(bind=angle_slider, max=6.28, left=200, value=starting_angle)

angle_label = wtext(text=space + str(starting_angle))
scene.append_to_caption('\n')
time_label = wtext(text=space + "Time : NULL")
scene.append_to_caption('\n')
current_angel_label = wtext(text=space + "Current Angle: NULL")
scene.append_to_caption('\n')
ang_vel_label = wtext(text=space + "Angular Velocity: " + str(rx))
scene.append_to_caption('\n')
x_label = wtext(text=space + "X: NULL")
scene.append_to_caption('\n')
vel_x_label = wtext(text=space + "Vel X: NULL")


# Algorithms
def turn(direction):
    test.rot_v += (torque / m0) * dt * direction


def slowdown():
    global stop
    if abs(test.rot_v) > 0.001:
        if test.rot_v > 0:
            turn(-1)
        else:
            turn(1)
    else:
        pass


def go_rotate():
    global stop
    global tar_angle
    global starting_angle
    # slowdown()
    if pi > tar_angle - starting_angle > 0 or tar_angle + 2 * pi - starting_angle < pi:
        used_angle = tar_angle - starting_angle
        if used_angle < 0:
            used_angle += 2 * pi
        print(str(used_angle) + " ONE")
        # if tar_angle < starting_angle: tar_angle += 2*pi
        if turn_t < sqrt(used_angle / (torque / m0)):
            turn(1)
        else:
            if turn_t < 2 * sqrt(used_angle / (torque / m0)):
                turn(-1)
            else:
                slowdown()
    else:
        used_angle = starting_angle - tar_angle
        if used_angle < 0:
            used_angle += 2 * pi
        print(str(used_angle) + " TWO")
        if turn_t < sqrt(used_angle / (torque / m0)):
            turn(-1)
        else:
            if turn_t < 2 * sqrt(used_angle / (torque / m0)):
                turn(1)
            else:
                slowdown()


while True and not stop:
    rate(animation_speed / dt)
    go_rotate()

    test.pos += test.vel * dt

    test.rotate(test.rot_v * dt, vec(0, 0, 1))
    test.angle += test.rot_v * dt

    time_label.text = space + "Time : " + '%.3f' % t
    current_angel_label.text = space + "Current Angle: " + str(test.angle % (2 * pi))
    ang_vel_label.text = space + "Angular Velocity: " + str('%.3f' % test.rot_v)
    x_label.text = space + "X: " + str('%.3f' % test.pos.x)
    vel_x_label.text = space + "Vel X:" + str('%.3f' % test.vel.x)

    f1.plot(t, test.angle)
    t += dt
    turn_t += dt
