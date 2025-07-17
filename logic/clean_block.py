def clean_block(destination, z_value, g0_xy_feed, g1_xy_feed, x_value, y_value, x_end, y_end, z_feed, waveform: str):
    destination.write(f"; Clean Block Start ({waveform} waveform)\n")

    # Existing initial G-code (if any)
    # Example: Go to start of cleaning area
    # destination.write(f"G0 X{x_value} Y{y_value} Z{z_value} F{g0_xy_feed}\n")

    if waveform == "sawtooth":
        destination.write("; Generating Sawtooth Clean Pattern\n")
        # --- YOUR SAWTOOTH CLEANING G-CODE HERE ---
        # Example: Clean with a wavy path within the block.
        # This could involve sweeping the area with small Y oscillations.
        
        # Placeholder for complex wavy cleaning path
        destination.write(f"G1 X{x_end:.3f} Y{y_end:.3f} Z{z_value:.3f} F{g1_xy_feed}\n")


    elif waveform == "square":
        destination.write("; Generating Square Wave Clean Pattern\n")
        # --- YOUR SQUARE CLEANING G-CODE HERE ---
        # Example: Standard rectilinear cleaning pattern, or a pattern with sharp turns.
        # A simple back-and-forth cleaning motion.
        
        # Placeholder for standard cleaning path
        destination.write(f"G1 X{x_end:.3f} Y{y_end:.3f} Z{z_value:.3f} F{g1_xy_feed}\n")

    else:
        destination.write(f"; Warning: Unknown waveform '{waveform}'. Generating default clean pattern.\n")
        # --- DEFAULT CLEANING G-CODE HERE (e.g., your original clean block logic) ---
        destination.write(f"G1 X{x_end:.3f} Y{y_end:.3f} Z{z_value:.3f} F{g1_xy_feed}\n")

    destination.write("; Clean Block End\n")
    return 0 # Assuming this function returns 0