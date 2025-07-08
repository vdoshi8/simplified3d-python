from typing import TextIO
def print_block(
    destination: TextIO,
    z_value: float,
    g0_xy_feed: str,
    g1_xy_feed: str,
    square_button: bool,
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
) -> bool:
    """
    Reimplementation of VB.NET printBlock.

    :param destination: file-like object to write G-code lines to
    :param z_value: current Z height
    :param g0_xy_feed: feed string to use for G0 moves
    :param g1_xy_feed: feed string to use for G1 moves
    :param square_button: True for square pattern, False for sawtooth
    :param deposition: True if depositing material (use G1), False for rapid moves (G0)
    :param x_value: X coordinate
    :param y_value: Y coordinate
    :param vertical_lift: amount to lift before move
    :param delay_time: dwell time (P parameter for G04)
    :param step_button: whether step/ultrasound logic applies
    :param ultrasound_state: current ultrasound on/off state
    :param z_feed: feed rate for Z moves
    :param next_tool_angle: target A-axis angle
    :param a_feed: feed rate for A moves
    :return: updated ultrasound_state
    """

    # 1) Lift Z, set feed rate
    destination.write(f"G1 Z{z_value + vertical_lift} F{z_feed}\n")

    # 2) Rotate A axis
    destination.write(f"G1 A{next_tool_angle} F{a_feed}\n")

    # 3) Build the X/Y move line
    cmd = "G1" if deposition else "G0"
    if square_button:
        # TODO: implement square-pattern logic here,
        # e.g. using x_value, y_value, g1_xy_feed
        xy_line = f"{cmd} X{x_value} Y{y_value} F{g1_xy_feed}"
    else:
        # TODO: implement zigzag (sawtooth) logic here,
        # e.g. using g0_xy_feed
        xy_line = f"{cmd} X{x_value} Y{y_value} F{g0_xy_feed}"

    destination.write(xy_line + "\n")
    if not deposition:
        destination.write(f"G1 Z{z_value} F{z_feed}\n")
    destination.write(f"G04 P{delay_time}\n")
    if step_button and ultrasound_state:
        # TODO:
        ultrasound_state = not ultrasound_state

    return ultrasound_state
