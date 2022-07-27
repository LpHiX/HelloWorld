from vpython import *

func_graph = gcurve(color=color.cyan)
func_graph_ecm = gcurve(color=color.green)

def func(t, x):
    try:
        function = cos(x*t)
    except OverflowError:
        function = float(0)
    return function


t = 0
x = 0.9

dt = 0.01
x_ecm = x

while t < 100:
    rate(1/dt)

    k1 = func(t, x)
    k2 = func(t+dt/2, x+dt*k1/2)
    k3 = func(t+dt/2, x+dt*k2/2)
    k4 = func(t+dt, x+dt*k3)

    x = x+ dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    t += dt

    x_ecm = x_ecm + func(t, x) * dt

    func_graph.plot(pos=(t, x))
    func_graph_ecm.plot(pos=(t, x_ecm))
