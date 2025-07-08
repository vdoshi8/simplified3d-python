# logic/print_zigzag.py

def print_zigzag(destination, x_start, x_end, y_value, z_value, passes, feedrate):
    destination.write(f"; Print ZigZag Start\n")
    direction = 1
    for i in range(passes):
        x1 = x_start if direction > 0 else x_end
        x2 = x_end if direction > 0 else x_start
        destination.write(f"G1 X{x1} Y{y_value + i*0.2:.3f} Z{z_value} F{feedrate}\n")
        destination.write(f"G1 X{x2} Y{y_value + i*0.2:.3f} Z{z_value} F{feedrate}\n")
        direction *= -1
    destination.write(f"; Print ZigZag End\n")
