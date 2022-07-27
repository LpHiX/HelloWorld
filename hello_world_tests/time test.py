import time
import matplotlib.pyplot as plt

t = 0
dt = 0.001
start_time = time.time()

fig = plt.figure()
ax1 = fig.add_subplot(111)
x = []
y = []

while t < 10:
    print(t, time.time() - start_time, time.time() - start_time - t)
    time.sleep(dt)
    x.append(time.time() - start_time)
    y.append(time.time() - start_time - t)
    t += dt
ax1.plot(x,y)
plt.show()
