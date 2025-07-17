from math import cos, sin, pi

def print_cylinder(destination, x_center, y_center, z_value, radius, segments, feedrate, waveform: str):
    destination.write(f"; Print Cylinder Start ({waveform} waveform)\n")

    # Calculate the angle increment for each segment
    angle_increment = 2 * pi / segments

    for i in range(segments + 1):
        angle = i * angle_increment

        if waveform == "sawtooth":
            # --- Sawtooth Waveform Logic for a cylinder/circle ---
            # For a cylinder, a sawtooth could mean the radius oscillates slightly
            # or there's a small radial "sawtooth" pattern as it draws.
            # Example: Vary radius based on angle (simple sawtooth)
            sawtooth_amplitude = 0.2 * radius # Example: 20% of radius
            # Simple oscillation, could be more complex
            current_radius = radius + sawtooth_amplitude * ((angle % (2 * pi / 4)) / (2 * pi / 4) - 0.5) # Example oscillation

            x = x_center + current_radius * cos(angle)
            y = y_center + current_radius * sin(angle)

        elif waveform == "square":
            # --- Square Waveform Logic for a cylinder/circle ---
            # For a cylinder, a square wave could mean approximating a circle
            # with straighter segments that form "blocks" or "steps".
            # Example: snapping to cardinal directions or forming a polygon with flat sides.
            # A simple "square wave" around a circle might involve stepping between
            # discrete angles that approximate a square or octagonal shape.

            # For simplicity, let's imagine a square wave on a circle means
            # it alternates between two radii or snaps to an outer/inner boundary
            # for certain angular segments, creating a "blocky" circle.
            # Or, it could create a square-like shape instead of a circle.

            # Let's simplify and make it draw a SQUARE rather than a circle
            # if the "square" waveform is selected, for demonstration.
            # You'll need to define points for a square path.

            # If i is 0 or multiple of segments/4, it's a corner or cardinal point
            # This is just an idea, exact implementation depends on desired "square"

            # For a "square" around a point, you might draw a square instead of a circle.
            # This would need different logic, potentially abandoning the angle loop for a
            # sequence of G1 moves for a square.

            # Reverting to basic circle if "square" means just a solid circle without oscillation
            # as the concept of a "square wave" on a circle is abstract.
            x = x_center + radius * cos(angle)
            y = y_center + radius * sin(angle)

        else:
            # Default to normal circular path if waveform is unknown
            x = x_center + radius * cos(angle)
            y = y_center + radius * sin(angle)

        # G1: Linear interpolation move
        destination.write(f"G1 X{x:.3f} Y{y:.3f} Z{z_value:.3f} F{feedrate}\n")

    destination.write("; Print Cylinder End\n")
    