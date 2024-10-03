import pgzrun
import math
import random

WIDTH = 800
HEIGHT = 600

RADIUS = 100
TUBE_RADIUS = 40
DOT_MULTIPLYER = 2
NUM_DOTS = int(96 * DOT_MULTIPLYER)
NUM_TUBE = int(48 * DOT_MULTIPLYER)

angle_x = 0
angle_y = 0

LIGHT_DIR = (1, -1, 1)
LIGHT_DIR = tuple(l / math.sqrt(sum(x**2 for x in LIGHT_DIR)) for l in LIGHT_DIR)

def update():
    global angle_x, angle_y
    angle_x += 0.02
    angle_y += 0.01

def draw():
    screen.fill((0, 0, 0))
    ambient_light = 0.1
    dots = []

    for i in range(NUM_DOTS):
        for j in range(NUM_TUBE):
            theta = (i / NUM_DOTS) * 2 * math.pi
            phi = (j / NUM_TUBE) * 2 * math.pi

            x = (RADIUS + TUBE_RADIUS * math.cos(phi)) * math.cos(theta)
            y = (RADIUS + TUBE_RADIUS * math.cos(phi)) * math.sin(theta)
            z = TUBE_RADIUS * math.sin(phi)

            normal = (
                math.cos(phi) * math.cos(theta),
                math.cos(phi) * math.sin(theta),
                math.sin(phi)
            )

            normal_y_rotated = normal[0] * math.cos(angle_y) + normal[2] * math.sin(angle_y)
            normal_z_rotated = -normal[0] * math.sin(angle_y) + normal[2] * math.cos(angle_y)
            normal_x_rotated = normal[1] * math.cos(angle_x) - normal_z_rotated * math.sin(angle_x)
            normal_z_final = normal[1] * math.sin(angle_x) + normal_z_rotated * math.cos(angle_x)

            dot_product = (normal_y_rotated * LIGHT_DIR[0] +
                           normal_x_rotated * LIGHT_DIR[1] +
                           normal_z_final * LIGHT_DIR[2])
            intensity = max(0.0, dot_product)
            color_value = int(255 * (ambient_light + intensity * (1 - ambient_light)))
            # color = (color_value, 0, 255 - color_value)
            color = (random.randint(0,225),0,0)

            y_rotated = y * math.cos(angle_x) - z * math.sin(angle_x)
            z_rotated = y * math.sin(angle_x) + z * math.cos(angle_x)
            x_rotated = x * math.cos(angle_y) + z_rotated * math.sin(angle_y)

            z_projected = z_rotated
            x_proj = int(WIDTH / 2 + x_rotated)
            y_proj = int(HEIGHT / 2 - y_rotated)

            dots.append((x_proj, y_proj, z_projected, color))

    dots.sort(key=lambda dot: dot[2])

    for x_proj, y_proj, z_projected, color in dots:
        screen.draw.filled_circle((x_proj, y_proj), 5, color)

pgzrun.go()