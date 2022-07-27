from vpython import *

g = 9.81
dt = 0.001
animation_speed = 1
m = 1000
radius = 0.5
starting_speed = 20
t = 0
mover_speed = 10

surface_air_density = 5.225
wind_vel = vec(-50, 0, -500)


scene = canvas(width=800, height=800)
plat = box(size=vec(10, 0.1, 10), pos=vec(0, -0.05, 0), opacity=1, color=vec(0.5, 1, 0.5))


def air_density(h):
    return surface_air_density * pow(0.999, h / 10)


def drag_force(vel):
    vel_dif = vel - wind_vel
    return -vel_dif.mag * vel_dif * 0.5 * air_density(test.height) * radius**2 * pi * 0.47 / m


def gravity_force():
    return vec(0, -g, 0)


for x in range(0, 15):
    test = sphere(radius=radius, pos=vec(0, radius, 0), make_trail=True)
    test.vel = vec(cos(x * pi / 30) * starting_speed, sin(x * pi / 30) * starting_speed, 0)
    while test.pos.y >= radius:
        rate(animation_speed/dt)
        test.pos += test.vel * dt
        test.vel += (drag_force(test.vel) + gravity_force()) * dt

        k = keysdown()
        if 'up' in k: test.vel.y += mover_speed  * 2 * dt
        if 'down' in k: test.vel.y -= mover_speed * dt
        if 'right' in k: test.vel.x += mover_speed * dt
        if 'left' in k: test.vel.x -= mover_speed * dt

        t += dt
        print(test.pos.y)

print("Complete")