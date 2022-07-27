from vpython import *
import numpy as np

scene = canvas(width=500, height=500)
f1 = gcurve(color=color.cyan)

rocket = box(pos=vec(0, 35, 0), size=vec(70, 3.7, 3.7), color=vec(0, 0.5, 1), make_trail=True)
nozzle = pyramid(pos=vec(-35, 35, 0), size=vec(10, 10, 10), color=vec(0, 1, 0))
ascent_profile = curve(vec(0, 0, 0))

F = 7607000
m0 = 549000
dt = 0.001
animation_speed = 1
moment_of_inertia = 204737
ascent_multiplier = 200

p0 = 0.5
i0 = 0.5
d0 = 0.5
p1 = 10
i1 = 2
d1 = 100
p2 = 10
i2 = 2
d2 = 100

surface_air_density = 0
wind_vel = vec(0, 0, 0)

t = 0
g = 9.81
throttle = 1
m = m0
tar_nozzle_angle = 0
tar_rocket_angle = 0
nozzle.angle = -pi
rocket.angle = 0
rocket.vel = vec(0, 0, 0)
rocket.ang_vel = 0
rocket.torque = 0
rocket.ang_accel = 0
rocket.landed = False

landing = False


def setup_ascent_visualizer(x_interval, y_multiplier, multiples):
    for i in range(0, multiples):
        ascent_profile.append(vec(x_interval * i ** 2, y_multiplier * sqrt(x_interval * i ** 2), 0))


def rotate_nozzle(angle):
    nozzle.rotate(angle, vec(0, 0, 1))
    nozzle.angle += angle
    pass


def rotate_rocket(angle):
    rocket.rotate(angle, vec(0, 0, 1))
    rocket.angle += angle
    nozzle.rotate(angle, vec(0, 0, 1), origin=rocket.pos)

    if rocket.angle <= -pi: rocket.angle += 2 * pi
    if rocket.angle >= pi: rocket.angle -= 2 * pi


def animation_slider(slider_value):
    global animation_speed
    animation_speed = slider_value.value


def rocket_throttle(slider_value):
    global throttle
    throttle = slider_value.value


def target_rocket_slider(slider_value):
    global tar_rocket_angle
    tar_rocket_angle = slider_value.value
    rotate_rocket(tar_rocket_angle - rocket.angle)


def landing_button(b):
    global landing, angle_pid_integral, trajectory_pid_integral_error, last_pid_angle_error, last_pid_trajectory_error, landing_x
    angle_pid_integral = 0
    trajectory_pid_integral_error = 0
    last_pid_angle_error = 0
    last_pid_trajectory_error = 0
    landing = True


def move(pos):
    rocket.pos += pos * dt
    nozzle.pos += pos * dt


vel_vec = arrow(shaftwidth=1, color=color.green)
rocket_force_vec = arrow(shaftwidth=1, color=color.yellow)
ang_force_vec = arrow(shaftwidth=1, color=color.orange)
drag_force_vec = arrow(shaftwidth=1, color=color.red)
gravity_force_vec = arrow(shaftwidth=1, color=color.cyan)


def rocket_force():
    global throttle
    if not rocket.landed:
        force_x = F * cos(rocket.angle) * cos(nozzle.angle) * throttle
        force_y = F * sin(rocket.angle) * cos(nozzle.angle) * throttle
        if not landing:
            throttle = 1
            nozzle.color = vec(1, 1, 0)
            rocket_force_vec.axis = vec(force_x / m, force_y / m, 0)
            rocket_force_vec.pos = rocket.pos + vec(20, 0, 0)
            return vec(force_x, force_y, 0)
        elif rocket.pos.y - 35 <= rocket.vel.y ** 2 / ((F / m) - g) and rocket.vel.y < 0:
            throttle = 1
            nozzle.color = vec(1, 0, 0)
            rocket_force_vec.axis = vec(force_x / m, force_y / m, 0)
            rocket_force_vec.pos = rocket.pos + vec(20, 0, 0)
            return vec(force_x, force_y, 0)
        else:
            if rocket.pos.y > 35.2:
                nozzle.color = vec(1, 1, 1)
                throttle = 0.1
                rocket_force_vec.axis = vec(force_x * 0.1 / m, force_y * 0.1 / m, 0)
                rocket_force_vec.pos = rocket.pos + vec(20, 0, 0)
                return vec(force_x * throttle, force_y * throttle, 0)
            else:
                throttle = 0
                print("LANDED")
                print("\nRocket Angle = " + str('%0.10f' % (rocket.angle * 180 / pi)) +
                      "\nNozzle Angle = " + str('%0.10f' % nozzle.angle) +
                      "\nX =" + str('%0.10f' % rocket.pos.x) +
                      "\nY =" + str('%0.10f' % rocket.pos.y) +
                      "\nX Velcoity =" + str('%0.10f' % rocket.vel.x) +
                      "\ny Velcoity =" + str('%0.10f' % rocket.vel.y) +
                      "\nVelcoity =" + str('%0.10f' % rocket.vel.mag) +
                      "\nTime =" + str('%0.3f' % t))
                rocket.landed = True
                rocket_force_vec.visible = False
                rocket_force_vec.pos = rocket.pos + vec(20, 0, 0)
                return vec(0, 0, 0)
    return vec(0, 0, 0)


# The force calculations and calculations for rotating the rocket, this is done in the main loop, many times per second
def rocket_ang_force():
    # To find the torque of the rocket from the angle of nozzle * force of nozzle
    rocket.torque = -F * sin(nozzle.angle) * 2
    # Converting the torque force into angular acceleration
    rocket.ang_accel = rocket.torque * throttle / (moment_of_inertia * (m / m0))

    if rocket.landed:
        rocket.ang_accel = 0

    rocket.ang_vel += cos(nozzle.angle) * rocket.ang_accel * dt * throttle
    # Display ing rotational vectors
    ang_force_vec.axis = rocket.ang_vel * vec(cos(rocket.angle - pi / 2), sin(rocket.angle - pi / 2), 0) * 100
    ang_force_vec.pos = nozzle.pos - rocket.ang_vel * vec(cos(rocket.angle - pi / 2), sin(rocket.angle - pi / 2),
                                                          0) * 100
    # Using the velocity to rotate the rocket
    rotate_rocket(rocket.ang_vel * dt)


def air_density(h):
    return surface_air_density * pow(0.999, h / 10)


def drag_force(vel):
    vel_dif = vel - wind_vel

    vel_angle = atan2(vel.y, vel.x)
    surface_area = abs(70 * sin(rocket.angle - vel_angle) + 3.7 * cos(rocket.angle - vel_angle)) * 3.7

    drag_force_value = -vel_dif.mag * vel_dif * 0.5 * air_density(rocket.pos.y) * surface_area * 1

    drag_force_vec.axis = drag_force_value * 10 / m
    drag_force_vec.pos = rocket.pos + vec(20, 0, 1)

    return drag_force_value


def gravity_force():
    gravity_force_vec.axis = vec(0, -g, 0)
    gravity_force_vec.pos = rocket.pos + vec(20, 0, -1)
    return vec(0, -g, 0) * m


def detect_collide():
    if rocket.pos.y - (abs(35 * sin(rocket.angle))) < 0:
        rocket.vel.y = rocket.vel.y * -0.1
        move(vec(0, 1, 0))


last_pid_angle_error = 0
angle_pid_integral = 0


def pid_angle():
    global last_pid_angle_error
    global angle_pid_integral
    if not landing:
        profile_angle = -atan2(rocket.pos.y / ((ascent_multiplier ** 2) / 2), 1)
    else:
        profile_angle = atan2(rocket.vel.y, rocket.vel.x) + pi / 2
    pid_error = rocket.angle - pi / 2 - profile_angle
    if pid_error <= -pi: pid_error += 2 * pi
    if pid_error >= pi: pid_error -= 2 * pi

    d_pid_error = -(last_pid_angle_error - pid_error) / dt

    pid_value = pid_error * p0 + d_pid_error * d0
    final_value = np.sign(pid_value) * (1 / 4) * (abs(pid_value)) ** (2 / 3)

    last_pid_angle_error = pid_error
    return final_value


last_pid_trajectory_error = 0
trajectory_pid_integral_error = 0


def pid_trajectory():
    global last_pid_trajectory_error
    global trajectory_pid_integral_error
    profile_x = (1 / ascent_multiplier ** 2) * rocket.pos.y ** 2
    pid_error = rocket.pos.x - profile_x
    if landing: pid_error = 0

    d_pid_error = -(last_pid_trajectory_error - pid_error) / dt

    pid_value = pid_error * p1 + d_pid_error * d1 + trajectory_pid_integral_error * i1
    final_pid_value = np.sign(pid_value) * (-1 / 50) * (abs(pid_value)) ** (2 / 9)
    last_pid_trajectory_error = pid_error

    trajectory_pid_integral_error += pid_error * dt
    return final_pid_value


last_pid_landing_error = 0
landing_pid_integral_error = 0


def pid_landing():
    if landing:
        global last_pid_landing_error
        global landing_pid_integral_error
        pid_error = rocket.vel.x

        d_pid_error = (last_pid_landing_error - pid_error) / dt

        pid_value = pid_error * p2 + d_pid_error * d2 + landing_pid_integral_error * i2
        final_pid_value = np.sign(pid_value) * (1 / 50) * (abs(pid_value)) ** (2 / 9)
        last_pid_landing_error = pid_error

        landing_pid_integral_error += pid_error * dt
        # print(-final_pid_value)
        return 0
    return 0


scene.append_to_caption("\n\n")
slider(bind=animation_slider, min=0.1, max=10, value=1)
scene.append_to_caption("\n\n")
slider(bind=rocket_throttle, min=0, max=10, value=1)
scene.append_to_caption("\n\n")
slider(bind=target_rocket_slider, min=-pi / 2, max=3 * pi / 2, value=pi / 2)
scene.append_to_caption("\n\n")
button(bind=landing_button, text="Land")
angle_label = wtext(text="\nText Display Setup...")

rotate_rocket(pi / 2)
rotate_nozzle(pi)
stop = False
scene.autoscale = False
scene.camera.follow(rocket)
setup_ascent_visualizer(3, ascent_multiplier, 10000)
plat = box(size=vec(100000, 0.5, 100000), pos=vec(0, -0.05, 0), opacity=0.2, color=vec(0.5, 1, 0.5))
under = box(size=vec(10, 1, 10), pos=vec(0, -0.05, 0), opacity=0.5, color=vec(0.5, 1, 0.5))
landing_target = box(size=vec(10, 1, 10), pos=vec(1000, -0.05, 0), opacity=1, color=vec(0.5, 0, 0.5))

while True and not stop:
    rate(animation_speed / dt)

    pid_a = pid_angle()
    pid_t = pid_trajectory()
    pid_l = pid_landing()

    net_force = rocket_force() + gravity_force() + drag_force(rocket.vel)
    rocket_ang_force()
    rocket.vel += net_force * dt / m

    total_pid = pid_t + pid_a + pid_landing()
    if total_pid < -0.01: total_pid = -0.01
    if total_pid > 0.01: total_pid = 0.01

    move(rocket.vel)
    angle_label.text = "\nRocket Angle = " + str('%0.10f' % (rocket.angle * 180 / pi)) + \
                       "\nNozzle Angle = " + str('%0.10f' % nozzle.angle) + \
                       "\nX =" + str('%0.10f' % rocket.pos.x) + \
                       "\nY =" + str('%0.10f' % rocket.pos.y) + \
                       "\nY =" + str('%0.10f' % (rocket.vel.y ** 2 / ((F / m) - g))) + \
                       "\nY =" + str('%0.10f' % ((rocket.pos.y - rocket.vel.y ** 2 / ((F / m) - g)) - 35)) + \
                       "\nX Velcoity =" + str('%0.10f' % rocket.vel.x) + \
                       "\ny Velcoity =" + str('%0.10f' % rocket.vel.y) + \
                       "\nVelcoity =" + str('%0.10f' % rocket.vel.mag) + \
                       "\nPID Angle =" + str('%0.10f' % pid_a) + \
                       "\nPID Trajectory =" + str('%0.10f' % pid_t) + \
                       "\nTotal PID =" + str('%0.10f' % total_pid) + \
                       "\nRocket Force =" + str('%0.10f' % mag(rocket_force())) + \
                       "\nAir Density =" + str('%0.10f' % air_density(rocket.pos.y)) + \
                       "\nDrag =" + str('%0.10f' % mag(drag_force(rocket.vel))) + \
                       "\nTime =" + str('%0.3f' % t) + \
                       "\nLanding =" + str(landing)
    rotate_nozzle(total_pid - nozzle.angle + 0.005)
    detect_collide()

    vel_vec.axis = rocket.vel
    vel_vec.pos = rocket.pos + vec(20, 0, -2)
    under.pos.x = rocket.pos.x

    # if (t*100).__round__() % 100 == 0: f1.plot(t, nozzle.angle)
    t += dt
