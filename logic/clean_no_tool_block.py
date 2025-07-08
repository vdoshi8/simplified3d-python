# logic/clean_no_tool_block.py
def clean_no_tool_block(destination, x_value, y_value, z_value, z_feed, delay_time):
    destination.write(f"; Clean No Tool Block Start\n")
    # G0: Rapid positioning move
    # X, Y, Z: Target coordinates
    # F: Feedrate (for Z-axis movement or overall rapid movement)
    destination.write(f"G0 X{x_value} Y{y_value} Z{z_value} F{z_feed}\n")
    # G04: Dwell (pause) command
    # P: Pause duration in milliseconds
    destination.write(f"G04 P{delay_time}\n")
    destination.write(f"; Clean No Tool Block End\n")
