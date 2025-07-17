from typing import TextIO
import math

def print_block(
    destination: TextIO,
    z_value: float,
    g0_xy_feed: str,
    g1_xy_feed: str,
    deposition: bool,
    x_value: float,
    y_value: float,
    vertical_lift: float,
    delay_time: float,
    step_button: bool,
    ultrasound_state: bool,
    z_feed: int,
    next_tool_angle: float,
    a_feed: int,
    waveform: str,  # <-- NEW: Added waveform parameter
) -> bool:
    """
    Reimplementation of VB.NET printBlock.
    Updated to incorporate waveform-specific G-code generation.

    :param destination: file-like object to write G-code lines to
    :param z_value: current Z height
    :param g0_xy_feed: feed string to use for G0 moves
    :param g1_xy_feed: feed string to use for G1 moves
    :param deposition: True if depositing material (use G1), False for rapid moves (G0)
    :param x_value: X coordinate (interpreted as block start X)
    :param y_value: Y coordinate (interpreted as block start Y)
    :param vertical_lift: amount to lift before move
    :param delay_time: dwell time (P parameter for G04)
    :param step_button: whether step/ultrasound logic applies
    :param ultrasound_state: current ultrasound on/off state
    :param z_feed: feed rate for Z moves
    :param next_tool_angle: target A-axis angle
    :param a_feed: feed rate for A moves
    :param waveform: "sawtooth" or "square" to determine G-code pattern
    :return: updated ultrasound_state
    """

    destination.write(f"; Print Block Start ({waveform} waveform)\n")

    # 1) Lift Z, set feed rate
    destination.write(f"G1 Z{z_value + vertical_lift} F{z_feed}\n")

    # 2) Rotate A axis
    destination.write(f"G1 A{next_tool_angle} F{a_feed}\n")

    # Determine command based on deposition
    cmd = "G1" if deposition else "G0"

    # Define some example block dimensions for demonstration.
    # You'll likely need to pass these as parameters or retrieve them from elsewhere.
    block_width = 10.0
    block_height = 10.0

    if waveform == "sawtooth":
        destination.write("; Generating Sawtooth Block Pattern\n")
        # --- Sawtooth G-code for block outline ---
        # Example: A block outline with wavy edges.
        
        # Move to starting corner
        destination.write(f"G0 X{x_value:.3f} Y{y_value:.3f} Z{z_value:.3f} F{g0_xy_feed}\n")
        
        num_waves_x = 5
        wave_amplitude_y = 0.5 # Y oscillation for X segments
        
        # Draw top edge with waves
        for i in range(num_waves_x):
            seg_start_x = x_value + (block_width / num_waves_x) * i
            seg_end_x = x_value + (block_width / num_waves_x) * (i + 1)
            mid_x = seg_start_x + (seg_end_x - seg_start_x) / 2
            
            destination.write(f"{cmd} X{mid_x:.3f} Y{y_value + wave_amplitude_y:.3f} F{g1_xy_feed}\n")
            destination.write(f"{cmd} X{seg_end_x:.3f} Y{y_value:.3f} F{g1_xy_feed}\n")
            
        # Move to next corner (Y-axis for side)
        destination.write(f"{cmd} X{x_value + block_width:.3f} Y{y_value:.3f} F{g1_xy_feed}\n")

        num_waves_y = 5
        wave_amplitude_x = 0.5 # X oscillation for Y segments

        # Draw right edge with waves
        for i in range(num_waves_y):
            seg_start_y = y_value + (block_height / num_waves_y) * i
            seg_end_y = y_value + (block_height / num_waves_y) * (i + 1)
            mid_y = seg_start_y + (seg_end_y - seg_start_y) / 2
            
            destination.write(f"{cmd} X{x_value + block_width + wave_amplitude_x:.3f} Y{mid_y:.3f} F{g1_xy_feed}\n")
            destination.write(f"{cmd} X{x_value + block_width:.3f} Y{seg_end_y:.3f} F{g1_xy_feed}\n")
            
        # Move to next corner (X-axis for bottom)
        destination.write(f"{cmd} X{x_value + block_width:.3f} Y{y_value + block_height:.3f} F{g1_xy_feed}\n")

        # Draw bottom edge with waves (in reverse for consistency)
        for i in range(num_waves_x - 1, -1, -1):
            seg_start_x = x_value + (block_width / num_waves_x) * i
            seg_end_x = x_value + (block_width / num_waves_x) * (i + 1)
            mid_x = seg_start_x + (seg_end_x - seg_start_x) / 2
            
            destination.write(f"{cmd} X{mid_x:.3f} Y{y_value + block_height - wave_amplitude_y:.3f} F{g1_xy_feed}\n")
            destination.write(f"{cmd} X{seg_start_x:.3f} Y{y_value + block_height:.3f} F{g1_xy_feed}\n")

        # Move to next corner (Y-axis for left)
        destination.write(f"{cmd} X{x_value:.3f} Y{y_value + block_height:.3f} F{g1_xy_feed}\n")

        # Draw left edge with waves (in reverse)
        for i in range(num_waves_y - 1, -1, -1):
            seg_start_y = y_value + (block_height / num_waves_y) * i
            seg_end_y = y_value + (block_height / num_waves_y) * (i + 1)
            mid_y = seg_start_y + (seg_end_y - seg_start_y) / 2
            
            destination.write(f"{cmd} X{x_value - wave_amplitude_x:.3f} Y{mid_y:.3f} F{g1_xy_feed}\n")
            destination.write(f"{cmd} X{x_value:.3f} Y{seg_start_y:.3f} F{g1_xy_feed}\n")
        
        # Ensure it closes back to the start
        destination.write(f"{cmd} X{x_value:.3f} Y{y_value:.3f} F{g1_xy_feed}\n")

    elif waveform == "square":
        destination.write("; Generating Square Wave Block Pattern\n")
        # --- Square G-code for block outline ---
        # Example: A standard rectangular block.
        
        # Move to starting corner
        destination.write(f"G0 X{x_value:.3f} Y{y_value:.3f} Z{z_value:.3f} F{g0_xy_feed}\n")
        
        # Draw the outline of a square block
        destination.write(f"{cmd} X{x_value + block_width:.3f} Y{y_value:.3f} F{g1_xy_feed}\n")
        destination.write(f"{cmd} X{x_value + block_width:.3f} Y{y_value + block_height:.3f} F{g1_xy_feed}\n")
        destination.write(f"{cmd} X{x_value:.3f} Y{y_value + block_height:.3f} F{g1_xy_feed}\n")
        destination.write(f"{cmd} X{x_value:.3f} Y{y_value:.3f} F{g1_xy_feed}\n")

    else:
        destination.write(f"; Warning: Unknown waveform '{waveform}'. Generating default (square) block.\n")
        # --- DEFAULT G-CODE FOR BLOCK (will act like a simple square for unknown waveform) ---
        
        # Move to starting corner
        destination.write(f"G0 X{x_value:.3f} Y{y_value:.3f} Z{z_value:.3f} F{g0_xy_feed}\n")
        
        # Draw the outline of a square block
        destination.write(f"{cmd} X{x_value + block_width:.3f} Y{y_value:.3f} F{g1_xy_feed}\n")
        destination.write(f"{cmd} X{x_value + block_width:.3f} Y{y_value + block_height:.3f} F{g1_xy_feed}\n")
        destination.write(f"{cmd} X{x_value:.3f} Y{y_value + block_height:.3f} F{g1_xy_feed}\n")
        destination.write(f"{cmd} X{x_value:.3f} Y{y_value:.3f} F{g1_xy_feed}\n")


    if not deposition:
        destination.write(f"G1 Z{z_value} F{z_feed}\n")
    destination.write(f"G04 P{delay_time}\n")
    if step_button and ultrasound_state:
        # TODO: Implement step/ultrasound logic as needed.
        ultrasound_state = not ultrasound_state # Example toggle

    destination.write("; Print Block End\n")
    return ultrasound_state