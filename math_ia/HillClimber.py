import matplotlib.pyplot as plt
from numpy import *

theta_1=51.6444 * pi/180
theta_2=141.302 * pi/180
phi_0= 83.3163 * pi/180
phi_speed= 0.0645396 * pi/180
rho_0= 0.730049
day= 201.730
hk_longitude=114.1694 * pi/180
hk_latitude=22.3193 * pi/180

def angular_distance(x):
    longitude = (arctan2(cos(theta_1) * sin(phi_0 + phi_speed*x), cos(phi_0 + phi_speed*x)) + theta_2 - (2 * pi * ( rho_0 + (day/365) + (x/86164)))) % (2 * pi) - pi
    latitude = arctan((sin(theta_1) * sin(phi_0 + phi_speed*x)) / (sqrt((cos(phi_0 + phi_speed*x))**2 + (cos(theta_1) * sin(phi_0 + phi_speed*x))**2)))

    return sqrt(((longitude - hk_longitude) * cos(latitude))**2 + (latitude - hk_latitude)**2)


def long_func(x):
    return (arctan2(cos(theta_1) * sin(phi_0 + phi_speed*x), cos(phi_0 + phi_speed*x)) + theta_2 - (2 * pi * ( rho_0 + (day/365) + (x/86164)))) % (2 * pi) - pi

def lat_func(x):
    return arctan((sin(theta_1) * sin(phi_0 + phi_speed*x)) / (sqrt((cos(phi_0 + phi_speed*x))**2 + (cos(theta_1) * sin(phi_0 + phi_speed*x))**2)))


#t_list = linspace(0,10000,1000)
#x_list= long_func(t_list)
#y_list = lat_func(t_list)

x_list0 = linspace(0, 100000, 10000)
x_list = []
y_list = []
for i in x_list0:
    if angular_distance(i) < 0.353:
        x_list.append(i)
        y_list.append(angular_distance(i))

print(long_func(0))
print(lat_func(0))

'''fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# plot the function'''
plt.scatter(x_list,y_list)

# show the plot
plt.show()