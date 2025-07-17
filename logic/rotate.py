def rotate(destination, angle, a_feed, waveform: str):
    destination.write(f"; Rotate Start ({waveform} waveform)\n")

    if waveform == "sawtooth":
        destination.write("; Generating Sawtooth Rotation\n")
        # --- YOUR SAWTOOTH ROTATION G-CODE HERE ---
        # This could involve oscillating the A-axis around the target angle,
        # or performing the rotation in small steps with slight overshoots/undershoots.
        # Example: Rotate in steps with small "jumps"
        num_steps = 10
        angle_per_step = angle / num_steps
        oscillation_amplitude = 5 # degrees

        for i in range(num_steps):
            current_angle = (i + 1) * angle_per_step
            destination.write(f"G1 A{current_angle:.3f} F{a_feed}\n")
            if i < num_steps - 1: # Add oscillation between steps
                destination.write(f"G1 A{current_angle + oscillation_amplitude:.3f} F{a_feed}\n")
                destination.write(f"G1 A{current_angle:.3f} F{a_feed}\n")

    elif waveform == "square":
        destination.write("; Generating Square Wave Rotation\n")
        # --- YOUR SQUARE ROTATION G-CODE HERE ---
        # This could mean performing the rotation in sharp, distinct segments,
        # or perhaps alternating between two specific angles.
        # Example: Rotate to target, then back slightly, then to target again, creating a "step"
        
        target_angle_step = angle / 2 # Example, split into two "square" steps
        
        destination.write(f"G1 A{target_angle_step:.3f} F{a_feed}\n")
        destination.write(f"G1 A{target_angle_step - 10:.3f} F{a_feed}\n") # Small back step
        destination.write(f"G1 A{angle:.3f} F{a_feed}\n")

    else:
        destination.write(f"; Warning: Unknown waveform '{waveform}'. Generating default rotation.\n")
        # --- DEFAULT ROTATION G-CODE HERE ---
        destination.write(f"G1 A{angle:.3f} F{a_feed}\n")

    destination.write("; Rotate End\n")
    return 0 # Assuming this function returns 0