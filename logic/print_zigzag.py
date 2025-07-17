import math
from typing import TextIO

def print_zigzag(destination: TextIO, x_start: float, x_end: float, y_value: float, z_value: float, passes: int, feedrate: int, waveform: str):
    destination.write(f"; Print ZigZag Start ({waveform} waveform)\n")
    
    # You may adjust these values based on desired visual effect
    sawtooth_amplitude = 0.2  # Amplitude of Y oscillation for sawtooth
    square_step_height = 0.2  # Height of Y step for square wave

    for i in range(passes):
        # Calculate Y for the current pass
        current_y_pass = y_value + i * 0.2

        if waveform == "sawtooth":
            destination.write(f"; Generating Sawtooth ZigZag Pass {i+1}\n")
            
            # Start at x_start for each pass (can be adjusted)
            destination.write(f"G0 X{x_start:.3f} Y{current_y_pass:.3f} Z{z_value:.3f} F{feedrate}\n")

            # Simulate sawtooth along the X-axis for each zigzag segment
            num_segments_per_line = 10 # More segments = smoother wave
            segment_length = (x_end - x_start) / num_segments_per_line
            
            for j in range(num_segments_per_line + 1):
                x_current = x_start + j * segment_length
                
                # Apply sawtooth oscillation to Y
                if j % 2 == 0:
                    y_oscillate = current_y_pass
                else:
                    y_oscillate = current_y_pass + sawtooth_amplitude * (1 if i % 2 == 0 else -1) # Alternate direction per pass

                destination.write(f"G1 X{x_current:.3f} Y{y_oscillate:.3f} Z{z_value:.3f} F{feedrate}\n")
            
            # Reverse for the zag part if needed, or simply proceed to next pass
            # For a basic zigzag with wavy lines, you'd repeat the above, but in reverse X
            # Example: from x_end back to x_start with oscillation
            if (i + 1) < passes: # Don't draw reverse path on the last pass if it's not part of the final form
                 for j in range(num_segments_per_line + 1):
                    x_current = x_end - j * segment_length # Move back
                    
                    if j % 2 == 0:
                        y_oscillate = current_y_pass
                    else:
                        y_oscillate = current_y_pass + sawtooth_amplitude * (1 if i % 2 == 0 else -1)

                    destination.write(f"G1 X{x_current:.3f} Y{y_oscillate:.3f} Z{z_value:.3f} F{feedrate}\n")

        elif waveform == "square":
            destination.write(f"; Generating Square Wave ZigZag Pass {i+1}\n")
            
            # Start at x_start for each pass (can be adjusted)
            destination.write(f"G0 X{x_start:.3f} Y{current_y_pass:.3f} Z{z_value:.3f} F{feedrate}\n")

            # Simulate square wave along the X-axis for each zigzag segment
            num_steps_per_line = 5 # Number of up/down steps
            step_length = (x_end - x_start) / (num_steps_per_line * 2) # For up and down part of step

            current_x_pos = x_start
            current_y_pos = current_y_pass
            
            for j in range(num_steps_per_line):
                # Move horizontally
                current_x_pos += step_length
                destination.write(f"G1 X{current_x_pos:.3f} Y{current_y_pos:.3f} Z{z_value:.3f} F{feedrate}\n")
                
                # Move up/down (based on pass direction)
                current_y_pos += square_step_height * (1 if i % 2 == 0 else -1)
                destination.write(f"G1 X{current_x_pos:.3f} Y{current_y_pos:.3f} Z{z_value:.3f} F{feedrate}\n")

                # Move horizontally
                current_x_pos += step_length
                destination.write(f"G1 X{current_x_pos:.3f} Y{current_y_pos:.3f} Z{z_value:.3f} F{feedrate}\n")

                # Move back to original Y level for this pass
                current_y_pos = current_y_pass
                destination.write(f"G1 X{current_x_pos:.3f} Y{current_y_pos:.3f} Z{z_value:.3f} F{feedrate}\n")
            
            # Ensure it ends at x_end for the current pass
            destination.write(f"G1 X{x_end:.3f} Y{current_y_pass:.3f} Z{z_value:.3f} F{feedrate}\n")

        else:
            destination.write(f"; Warning: Unknown waveform '{waveform}'. Generating default ZigZag Pass {i+1}.\n")
            # --- Default ZigZag Logic (your original code) ---
            # This is your current logic for a standard zigzag pattern.
            x1 = x_start if i % 2 == 0 else x_end
            x2 = x_end if i % 2 == 0 else x_start
            
            # Move to start of line for current pass
            destination.write(f"G0 X{x1:.3f} Y{current_y_pass:.3f} Z{z_value:.3f} F{feedrate}\n")
            # Draw line to end
            destination.write(f"G1 X{x2:.3f} Y{current_y_pass:.3f} Z{z_value:.3f} F{feedrate}\n")

    destination.write(f"; Print ZigZag End\n")