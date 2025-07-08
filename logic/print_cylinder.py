# logic/print_cylinder.py
from math import cos, sin, pi

def print_cylinder(destination, x_center, y_center, z_value, radius, segments, feedrate):
    destination.write(f"; Print Cylinder Start\n")
    # Loop through the segments to create a full circle
    for i in range(segments + 1):
        # Calculate the angle for the current segment
        angle = 2 * pi * i / segments
        # Calculate X and Y coordinates on the circle
        x = x_center + radius * cos(angle)
        y = y_center + radius * sin(angle)
        # G1: Linear interpolation move
        # X, Y: Target coordinates for the current segment
        # Z: Constant Z-value for the cylinder layer
        # F: Feedrate for the linear movement
        destination.write(f"G1 X{x:.3f} Y{y:.3f} Z{z_value} F{feedrate}\n")
    destination.write(f"; Print Cylinder End\n")
