def get_x(current_line: str) -> float:
    """
    Extracts the X coordinate from a G-code line.
    """
    x_index = current_line.find('X')
    y_index = current_line.find('Y')
    if x_index == -1 or y_index == -1:
        return 0.0

    try:
        value_str = current_line[x_index + 1:y_index - 1]
        return float(value_str)
    except ValueError:
        return 0.0


def get_y(current_line: str) -> float:
    """
    Extracts the Y coordinate from a G-code line,
    stopping at E, F, or Z if present.
    """
    y_index = current_line.find('Y')
    if y_index == -1:
        return 0.0

    candidates = []
    for marker in ('E', 'F', 'Z'):
        idx = current_line.find(marker, y_index + 1)
        if idx != -1:
            candidates.append(idx)

    next_index = min(candidates) if candidates else len(current_line)
    if next_index == len(current_line):
        next_index += 1

    try:
        value_str = current_line[y_index + 1:next_index - 1]
        return float(value_str)
    except ValueError:
        return 0.0


def get_z(current_line: str) -> float:
    """
    Extracts the Z coordinate from a G-code line,
    stopping at E, F, or Y if present.
    """
    z_index = current_line.find('Z')
    if z_index == -1:
        return 0.0

    candidates = []
    for marker in ('E', 'F', 'Y'):
        idx = current_line.find(marker, z_index + 1)
        if idx != -1:
            candidates.append(idx)

    next_index = min(candidates) if candidates else len(current_line)
    if next_index == len(current_line):
        next_index += 1

    try:
        value_str = current_line[z_index + 1:next_index - 1]
        return float(value_str)
    except ValueError:
        return 0.0


