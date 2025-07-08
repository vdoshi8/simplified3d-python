# logic/rotate.py
from math import cos, sin, radians

def rotate(destination, current_angle, rotate_by, x_value, y_value, z_value, feedrate):
    """
    Example logic for Rotate (replace with real logic if needed).
    This function generates G-code to perform a rotation by moving to a new
    calculated X, Y position based on the rotation angle.
    """
    destination.write(f"; Rotate Start\n")
    # Convert angles to radians for trigonometric functions
    current_angle_rad = radians(current_angle)
    rotate_by_rad = radians(rotate_by)

    # Calculate the new angle after rotation
    new_angle_rad = current_angle_rad + rotate_by_rad

    # Calculate new X and Y coordinates (assuming rotation around origin for simplicity)
    # If rotating around a specific point, the math would be more complex.
    # For this example, we'll just use the provided x_value, y_value as a reference
    # and show a conceptual rotation. For a real rotation, you'd apply a rotation matrix
    # to existing coordinates or define a path.
    # Here, let's just move to a new point that implies rotation.
    # This is a placeholder; real rotation logic would depend on the geometry being rotated.
    # For a simple example, let's just move to a point relative to the original x,y
    # that changes with the angle.
    # A more robust 'rotate' would take a set of points and apply a rotation matrix to them.
    # For demonstration, we'll just move the tool to a new X, Y, Z.
    # Let's assume we are moving to a point that is 'x_value' distance from origin along
    # the new angle, and 'y_value' distance perpendicular to it.
    # This example will just move to x_value, y_value, z_value and then to a new point.

    # Move to the initial position
    destination.write(f"G0 X{x_value:.3f} Y{y_value:.3f} Z{z_value:.3f} F{feedrate}\n")

    # For a simple demonstration of 'rotation', let's just move the tool to a new X, Y
    # that is 'rotate_by' degrees away from the original (x_value, y_value) relative to origin.
    # This is a very simplified interpretation.
    # A more accurate rotation would involve transforming existing geometry.
    # Let's assume 'x_value' and 'y_value' are coordinates of a point to be "rotated"
    # and we are moving the tool to the new rotated position.
    # For simplicity, let's just move to a new arbitrary point to signify a "rotation action"
    # without complex geometry transformation.
    # Let's move to a point (x_value + 5*cos(new_angle_rad), y_value + 5*sin(new_angle_rad))
    # This is a conceptual move, not a true object rotation.
    rotated_x = x_value + 5 * cos(new_angle_rad)
    rotated_y = y_value + 5 * sin(new_angle_rad)

    destination.write(f"G1 X{rotated_x:.3f} Y{rotated_y:.3f} Z{z_value:.3f} F{feedrate}\n")
    destination.write(f"; Rotate End\n")

