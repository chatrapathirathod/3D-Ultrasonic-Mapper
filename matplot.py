import serial
import matplotlib.pyplot as plt
from math import sin, cos, radians
import pickle

# Change COM port here
ser = serial.Serial('COM6', 9600)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

X, Y, Z = [], [], []
points = []


print("Live 3D Mapping Started...")

while True:
    line = ser.readline().decode(errors='ignore').strip()

    if not line:
        continue

    parts = line.split(",")

    if len(parts) != 3:
        continue

    try:
        pan = float(parts[0])
        tilt = float(parts[1])
        d = float(parts[2])
    except ValueError:
        continue

    theta = radians(pan)
    phi = radians(tilt)

    x = d * cos(phi) * cos(theta)
    y = d * cos(phi) * sin(theta)
    z = d * sin(phi)

    points.append([x, y, z])
    


    X.append(x)
    Y.append(y)
    Z.append(z)

    ax.clear()
    ax.scatter(X, Y, Z, s=2)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.pause(0.01)

