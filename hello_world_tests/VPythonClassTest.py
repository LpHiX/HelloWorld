from vpython import *
import time

f1 = gcurve(color=color.cyan)

class Testicle:
    def __init__(self):
        self.visual = sphere()


test = Testicle()

t = 0
dt = 0.001
start_time = time.time()

text1 = wtext(text="1")
scene.append_to_caption("\n")
text2 = wtext(text="2")
scene.append_to_caption("\n")
text3 = wtext(text="3")

while True:
    rate(1 / dt)
    t += dt
    text1.text = t
    text2.text = time.time() - start_time
    text3.text = time.time() - start_time - t
    test.visual.pos.x += 0.001
    f1.plot(time.time() - start_time, time.time() - start_time - t)
