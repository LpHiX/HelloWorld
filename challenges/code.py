f = open("xyz.txt", "r+")
raw = f.readlines()
x = "\nx=\\left["
y = "\ny=\\left["
z = "\nz=\\left["
for line in raw:
    parts = line.split()
    x += parts[0] + ","
    y += parts[1] + ","
    z += parts[2] + ","
x = x.rstrip(x[-1])
y = y.rstrip(y[-1])
z = z.rstrip(z[-1])
x += "\\right]"
y += "\\right]"
z += "\\right]"

f.write(x)
f.write(y)
f.write(z)

print(x)
print(y)
print(z)