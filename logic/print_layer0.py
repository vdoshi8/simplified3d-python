import math # You might need math functions like sin, cos

def print_layer0(destination, x_start, y_start, x_end, y_end, z_value, feedrate, waveform: str):
    destination.write(f"; Print Layer0 Start ({waveform} waveform)\n")

    # G0: Rapid positioning move to the start point
    destination.write(f"G0 X{x_start} Y{y_start} Z{z_value}\n")

    if waveform == "sawtooth":
        # --- Sawtooth Waveform Logic for a line ---
        # This is a conceptual example. A sawtooth on a line would involve
        # moving back and forth in Y while progressing in X.

        # Let's say you want small "sawtooth" teeth along the line
        num_teeth = 10
        line_length = math.sqrt((x_end - x_start)**2 + (y_end - y_start)**2)
        if line_length > 0:
            dx = (x_end - x_start) / num_teeth
            dy_amplitude = 0.5 # Example amplitude for the tooth

            for i in range(num_teeth + 1):
                current_x = x_start + i * dx
                # Alternate Y for sawtooth effect
                if i % 2 == 0:
                    current_y = y_start 
                else:
                    current_y = y_start + dy_amplitude

                destination.write(f"G1 X{current_x:.3f} Y{current_y:.3f} Z{z_value:.3f} F{feedrate}\n")

        destination.write("; End of Saw-tooth Layer0\n")

    elif waveform == "square":
        # --- Square Waveform Logic for a line ---
        # For a "square" pattern along a line, it might involve small steps up/down in Y
        # or simply adhering more strictly to the start/end points with minimal deviation.
        # Here, let's assume it means a "blockier" path or perhaps a simpler straight line.

        # This could be a very basic straight line if "square" means no oscillation
        destination.write(f"G1 X{x_end:.3f} Y{y_end:.3f} Z{z_value:.3f} F{feedrate}\n")
        destination.write("; End of Square Wave Layer0 (Straight line for simplicity)\n")

    else:
        # Fallback for unexpected waveform values, or generate a default pattern
        destination.write(f"; Warning: Unknown waveform '{waveform}'. Generating default straight line.\n")
        destination.write(f"G1 X{x_end:.3f} Y{y_end:.3f} Z{z_value:.3f} F{feedrate}\n")

    destination.write("; Print Layer0 End\n")
    