# logic/print_layer0.py
def print_layer0(destination, x_start, y_start, x_end, y_end, z_value, feedrate):
    destination.write(f"; Print Layer0 Start\n")
    # G0: Rapid positioning move to the start point
    destination.write(f"G0 X{x_start} Y{y_start} Z{z_value} F{feedrate}\n")
    # G1: Linear interpolation move to the end point, performing the "print"
    destination.write(f"G1 X{x_end} Y{y_end} Z{z_value} F{feedrate}\n")
    destination.write(f"; Print Layer0 End\n")
