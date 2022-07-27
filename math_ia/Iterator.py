from numpy import *

theta_1=51.6433 * pi/180
theta_2=88.0366 * pi/180
phi_0=426.482 * pi/180
phi_v= 0.0645308 * pi/180
rho_0= 0.502551
day= 212.502
hk_longitude=114.169 * pi/180
hk_latitude=22.3193 * pi/180


def longitude_function(t):
    return (2*arctan(cos(theta_1) * sin(phi_0 + phi_v*t) / (sqrt(cos(phi_0 + phi_v*t)**2+(cos(theta_1) * sin(phi_0 + phi_v*t))**2) + cos(phi_0 + phi_v*t))) + theta_2 - (2 * pi * ( rho_0 + (day/365) + (t/86164)))) % (2 * pi) - pi


def longitude_derivative(t):
    return phi_v*cos(theta_1)/(cos(phi_0 + phi_v*t)**2+(cos(theta_1) * sin(phi_0 + phi_v*t))**2)-(2*pi/86164)


def latitude_function(t):
    return arctan((sin(theta_1) * sin(phi_0 + phi_v*t)) / (sqrt((cos(phi_0 + phi_v*t))**2 + (cos(theta_1) * sin(phi_0 + phi_v*t))**2)))


def newton_raphson(t_n):
    return t_n - (longitude_function(t_n)-hk_longitude)/longitude_derivative(t_n)


test = 1
time = 0
while not(2.063 < latitude_function(time) * 180/pi < 42.5756):
    t = time
    for N in range(0,9):
        t = newton_raphson(t)
    time = t
    print("Test: " + str(test) + " Time: " + str(round(time)) + " Latitude: " + str(latitude_function(round(time))*180/pi) + " Passing HK? " + str(2.063 < latitude_function(time) * 180/pi < 42.5756))
    test += 1
    time += 2 * pi / phi_v
