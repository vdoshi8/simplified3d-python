# logic/slicer.py
def slicer(destination, x_start, x_end, y_value, z_value, layers, feedrate):
    """
    Example logic for Slicer (replace with real slicing logic if needed).
    This function simulates a basic slicing operation by generating G-code
    for multiple layers, each printing a simple line.
    """
    destination.write(f"; Slicer Start\n")
    layer_height = 0.2  # Example layer height
    for i in range(layers):
        current_z = z_value + i * layer_height
        destination.write(f"; Layer {i+1} at Z={current_z:.3f}\n")
        # Move to start of the line for the current layer
        destination.write(f"G0 X{x_start:.3f} Y{y_value:.3f} Z{current_z:.3f} F{feedrate}\n")
        # Print the line for the current layer
        destination.write(f"G1 X{x_end:.3f} Y{y_value:.3f} Z{current_z:.3f} F{feedrate}\n")
    destination.write(f"; Slicer End\n")

