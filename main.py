import pgzrun
import math

# Set the dimensions of the window
WIDTH = 800
HEIGHT = 600

# Torus settings
RADIUS = 100  # Radius from the center to the center of the tube
TUBE_RADIUS = 40  # Radius of the tube
NUM_DOTS = 96  # Number of dots along the tube
NUM_TUBE = 48  # Number of dots around the tube

# Initialize angles for rotation
angle_x = 0
angle_y = 0

# Light direction (static)
LIGHT_DIR = (9, -1, 1)  # Direction of the light source

def update():
    global angle_x, angle_y
    angle_x += 0.02  # Slow increment for X-axis rotation
    angle_y += 0.01  # Slow increment for Y-axis rotation

def draw():
    screen.fill((0, 0, 0))  # Black background

    # Normalize light direction
    light_length = math.sqrt(LIGHT_DIR[0]**2 + LIGHT_DIR[1]**2 + LIGHT_DIR[2]**2)
    light_dir = (LIGHT_DIR[0] / light_length, LIGHT_DIR[1] / light_length, LIGHT_DIR[2] / light_length)

    # Ambient light factor
    ambient_light = 0.1

    # Loop over the number of dots to create the torus
    for i in range(NUM_DOTS):
        for j in range(NUM_TUBE):
            # Calculate the angles for each dot
            theta = (i / NUM_DOTS) * 2 * math.pi  # Angle around the center of the torus
            phi = (j / NUM_TUBE) * 2 * math.pi  # Angle around the tube

            # Calculate the 3D coordinates of the torus (before rotation)
            x = (RADIUS + TUBE_RADIUS * math.cos(phi)) * math.cos(theta)
            y = (RADIUS + TUBE_RADIUS * math.cos(phi)) * math.sin(theta)
            z = TUBE_RADIUS * math.sin(phi)

            # Calculate normal vector at the dot (before rotation)
            normal = (
                math.cos(phi) * math.cos(theta),
                math.cos(phi) * math.sin(theta),
                math.sin(phi)
            )

            # Rotate the normal vector by the same rotation applied to the object
            normal_y_rotated = normal[0] * math.cos(angle_y) + normal[2] * math.sin(angle_y)
            normal_z_rotated = -normal[0] * math.sin(angle_y) + normal[2] * math.cos(angle_y)
            normal_x_rotated = normal[1] * math.cos(angle_x) - normal_z_rotated * math.sin(angle_x)
            normal_z_final = normal[1] * math.sin(angle_x) + normal_z_rotated * math.cos(angle_x)

            # Calculate the dot product for lighting using the rotated normal vector
            dot_product = (normal_y_rotated * light_dir[0] +
                           normal_x_rotated * light_dir[1] +
                           normal_z_final * light_dir[2])
            intensity = max(0, dot_product)  # Clamp to [0, 1]

            # Calculate final color with ambient light
            color_value = int(255 * (ambient_light + intensity * (1 - ambient_light)))  # Adjust intensity with ambient
            color = (color_value, 0, 255 - color_value)  # Gradient from blue to red

            # Apply rotation around the X-axis
            y_rotated = y * math.cos(angle_x) - z * math.sin(angle_x)
            z_rotated = y * math.sin(angle_x) + z * math.cos(angle_x)

            # Apply rotation around the Y-axis
            x_rotated = x * math.cos(angle_y) + z_rotated * math.sin(angle_y)

            # Project to the center of the screen
            x_proj = int(WIDTH / 2 + x_rotated)
            y_proj = int(HEIGHT / 2 - y_rotated)  # Note: minus for correct vertical orientation

            # Draw the dot with the calculated color
            screen.draw.filled_circle((x_proj, y_proj), 5, color)

pgzrun.go()
