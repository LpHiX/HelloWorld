from vpython import *
import numpy as np

f1 = gcurve(color=color.cyan)
f2 = gcurve(color=color.cyan)
scene = canvas(width=500, height=500)


x = -10
y = 10
vx = 20
vy = -10
tar_x = 0
tar_y = 0

m0 = 500
F = 10000
a = F/m0

g = 10
p = 110
i = 0
d = 25

dt = 0.001
t = 0
last_x_error = 0
last_y_error = 0
integral_x_error = 0
integral_y_error = 0
pid_x = 0
pid_y = 0

animation_speed = 1
pid = True
stop = False

background = box(size=vec(20, 20, 0.1), pos=vec(0, 0, 0), opacity=.8, color=vec(0.2, 0.2, 0.1), )
test = box(pos=vec(x, y, 0), size=vec(2, 2, 1), make_trail=True, color=vec(0, 0, 1), trail_color=vec(0, 0.5, 0))
control = box(pos=vec(-10, 0, 0), size=vec(1, 1, 1))
tar_pos_display = box(pos=vec(tar_x, tar_y, 0), size=vec(.1, .1, 10), color=vec(1, 1, 1))
test.vel = vec(vx, vy, 0)
control.vel = vec(0, 0, 0)
scene.camera.follow(test)


def x_slider(slider_value):
    global tar_x
    tar_x = slider_value.value
    tar_pos_display.pos.x = tar_x


def y_slider(slider_value):
    global tar_y
    tar_y = slider_value.value
    tar_pos_display.pos.y = tar_y


def toggle_pid(button):
    global pid
    global pid_x
    global pid_y
    pid = not pid
    pid_x = 0
    pid_y = 0
    print(pid)


scene.append_to_caption("\n\n")
slider(bind=x_slider, max=20, min=-20, value=0)
scene.append_to_caption("\n\n")
slider(bind=y_slider, max=20, min=-20, value=0)
scene.append_to_caption("\n\n")
button(bind=toggle_pid, text="Toggle PID")


def pid_controller():
    global last_x_error
    global last_y_error
    global integral_x_error
    global integral_y_error
    global pid_y
    global pid_x

    x_error = tar_x - test.pos.x
    y_error = tar_y - test.pos.y
    dx_error = (x_error - last_x_error) / dt
    dy_error = (y_error - last_y_error) / dt

    pid_x = (p * x_error) + (d * dx_error) + (i * integral_x_error)
    pid_y = (p * y_error) + (d * dy_error) + (i * integral_y_error)

    #print("--------------------\nCurrent Y = " + str(test.pos.y) + "\nPID Y: " + str(pid_y), "\nY_error: " + str(y_error), "\nDY error: " + str(dy_error), "\nReal DY: " + str(test.vel.y), "\nTotal y error: ", str(integral_y_error))

    integral_x_error += x_error * dt
    integral_y_error += y_error * dt

    last_x_error = x_error
    last_y_error = y_error

def burn():
    global pid_y
    global pid_x
    if pid_x > a: pid_x = a
    if pid_x < -a: pid_x = -a
    if pid_y > a: pid_y = a
    if pid_y < -a: pid_y = -a

    # print("---------\n" + str('%.3f'%pid_y) + "\n" + str('%.3f'%test.vel.y))
    test.vel.y += pid_y * dt
    test.vel.x += pid_x * dt


while True and not stop:
    rate(animation_speed/dt)

    test.pos += test.vel * dt
    control.pos += control.vel * dt
    if control.pos.y < -10:
        control.pos.y = 10
        control.vel.y = 0

    test.vel.y -= g * dt
    #test.vel.x -= g * dt
    control.vel.y -= g * dt

    if pid:
        pid_controller()

    burn()

    f1.plot(t, test.pos.y)
    #f2.plot(t, test.pos.x)
    t += dt
