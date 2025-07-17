def clean_no_tool_block(destination, z_value, g0_xy_feed, x_value, y_value, x_end, y_end, z_feed, waveform: str):
    destination.write(f"; Clean No Tool Block Start ({waveform} waveform)\n")

    # Existing initial G-code (if any)
    # destination.write(f"G0 X{x_value} Y{y_value} Z{z_value} F{g0_xy_feed}\n")

    if waveform == "sawtooth":
        destination.write("; Generating Sawtooth No Tool Clean Pattern\n")
        # --- YOUR SAWTOOTH NO-TOOL CLEANING G-CODE HERE ---
        # Similar logic to clean_block, but without deposition/tool active M-codes
        
        # Placeholder
        destination.write(f"G0 X{x_end:.3f} Y{y_end:.3f} Z{z_value:.3f} F{g0_xy_feed}\n")

    elif waveform == "square":
        destination.write("; Generating Square Wave No Tool Clean Pattern\n")
        # --- YOUR SQUARE NO-TOOL CLEANING G-CODE HERE ---
        # Placeholder
        destination.write(f"G0 X{x_end:.3f} Y{y_end:.3f} Z{z_value:.3f} F{g0_xy_feed}\n")

    else:
        destination.write(f"; Warning: Unknown waveform '{waveform}'. Generating default no-tool clean pattern.\n")
        # --- DEFAULT NO-TOOL CLEANING G-CODE HERE ---
        destination.write(f"G0 X{x_end:.3f} Y{y_end:.3f} Z{z_value:.3f} F{g0_xy_feed}\n")

    destination.write("; Clean No Tool Block End\n")
    return 0 # Assuming this function returns 0