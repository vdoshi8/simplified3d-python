import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar, ttk
from typing import Optional

# Set up the project root for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Placeholder logic functions for demonstration if actual logic files are not present.
class MockFile:
    """A mock file object for writing G-code content to a string."""
    def __init__(self):
        self.content = []

    def write(self, text):
        self.content.append(text)

    def getvalue(self):
        return "".join(self.content)

def mock_print_block(destination, z_value, g0_xy_feed, g1_xy_feed, square_button, deposition, x_value, y_value, vertical_lift, delay_time, step_button, ultrasound_state, z_feed, next_tool_angle, a_feed):
    destination.write(f"; Mock Print Block G-code for Z={z_value}, X={x_value}, Y={y_value}\n")
    destination.write(f"G0 F{g0_xy_feed} X{x_value} Y{y_value} Z{z_value + vertical_lift}\n")
    destination.write(f"G1 F{g1_xy_feed} X{x_value} Y{y_value} Z{z_value}\n")
    return not ultrasound_state

def mock_get_x(line):
    import re
    match = re.search(r'X([-+]?\d*\.?\d+)', line)
    return float(match.group(1)) if match else None

def mock_get_y(line):
    import re
    match = re.search(r'Y([-+]?\d*\.?\d+)', line)
    return float(match.group(1)) if match else None

def mock_get_z(line):
    import re
    match = re.search(r'Z([-+]?\d*\.?\d+)', line)
    return float(match.group(1)) if match else None

def mock_clean_block(destination, x_value, y_value, z_value, z_feed, delay_time):
    destination.write(f"; Mock Clean Block G-code for X={x_value}, Y={y_value}, Z={z_value}\n")
    destination.write(f"G0 Z{z_value + 5} F{z_feed}\n")
    destination.write(f"G4 P{delay_time}\n")
    destination.write(f"G0 X{x_value} Y{y_value} Z{z_value}\n")

def mock_print_cylinder(destination, x_center, y_center, z_value, radius, segments, feedrate):
    import math
    destination.write(f"; Mock Print Cylinder G-code for R={radius} at ({x_center},{y_center},{z_value})\n")
    destination.write(f"G0 X{x_center + radius} Y{y_center} Z{z_value} F{feedrate}\n")
    destination.write(f"G1 F{feedrate}\n")
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = x_center + radius * math.cos(angle)
        y = y_center + radius * math.sin(angle)
        destination.write(f"G1 X{x:.3f} Y{y:.3f}\n")

def mock_clean_no_tool_block(destination, x_value, y_value, z_value, z_feed, delay_time):
    destination.write(f"; Mock Clean No Tool Block G-code for X={x_value}, Y={y_value}, Z={z_value}\n")
    destination.write(f"G0 Z{z_value + 10} F{z_feed}\n")
    destination.write(f"G4 P{delay_time}\n")
    destination.write(f"G0 X{x_value} Y{y_value} Z{z_value}\n")

def mock_print_layer0(destination, x_start, y_start, x_end, y_end, z_value, feedrate):
    destination.write(f"; Mock Print Layer0 G-code from ({x_start},{y_start}) to ({x_end},{y_end}) at Z={z_value}\n")
    destination.write(f"G0 X{x_start} Y{y_start} Z{z_value} F{feedrate}\n")
    destination.write(f"G1 X{x_end} Y{y_end} F{feedrate}\n")

def mock_rotate(destination, current_angle, rotate_by, x_value, y_value, z_value, feedrate):
    new_angle = (current_angle + rotate_by) % 360
    destination.write(f"; Mock Rotate G-code: Rotated from {current_angle} to {new_angle} degrees\n")
    destination.write(f"G0 X{x_value} Y{y_value} Z{z_value} F{feedrate}\n")
    destination.write(f"M106 S{new_angle} ; Assuming M106 controls rotation/angle\n")
    return new_angle

def mock_slicer(destination, x_start, x_end, y_value, z_value, layers, feedrate):
    destination.write(f"; Mock Slicer G-code for {layers} layers\n")
    layer_height = 0.2
    for i in range(layers):
        current_z = z_value + i * layer_height
        destination.write(f"; Layer {i+1} at Z={current_z:.3f}\n")
        destination.write(f"G0 X{x_start} Y{y_value} Z{current_z} F{feedrate}\n")
        destination.write(f"G1 X{x_end} Y{y_value} F{feedrate}\n")
        destination.write(f"G0 X{x_end} Y{y_value + 1} Z{current_z} F{feedrate}\n")
        destination.write(f"G1 X{x_start} Y{y_value + 1} F{feedrate}\n")

def mock_print_zigzag(destination, x_start, x_end, y_value, z_value, passes, feedrate):
    destination.write(f"; Mock Print ZigZag G-code for {passes} passes at Z={z_value}\n")
    y_increment = 1.0
    current_y = y_value
    for i in range(passes):
        destination.write(f"G0 Z{z_value} F{feedrate}\n")
        if i % 2 == 0:
            destination.write(f"G0 X{x_start} Y{current_y} F{feedrate}\n")
            destination.write(f"G1 X{x_end} Y{current_y} F{feedrate}\n")
        else:
            destination.write(f"G0 X{x_end} Y{current_y} F{feedrate}\n")
            destination.write(f"G1 X{x_start} Y{current_y} F{feedrate}\n")
        current_y += y_increment
    destination.write(f"G0 Z{z_value + 5} F{feedrate}\n")

# Assign mock functions to the names expected by the UI.
# If you have actual logic files, comment out these assignments and import them.
print_block = mock_print_block
get_x = mock_get_x
get_y = mock_get_y
get_z = mock_get_z
clean_block = mock_clean_block
print_cylinder = mock_print_cylinder
clean_no_tool_block = mock_clean_no_tool_block
print_layer0 = mock_print_layer0
rotate = mock_rotate
slicer = mock_slicer
print_zigzag = mock_print_zigzag


# Global variables to hold the Text widgets and StringVar for tool selection
gcode_text_widget: Optional[Text] = None
result_text_widget: Optional[Text] = None
tool_selection_var: Optional[tk.StringVar] = None
status_var: Optional[tk.StringVar] = None

def show_tooltip(widget, text):
    """Add a simple tooltip to a widget."""
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.overrideredirect(True)
    label = tk.Label(tooltip, text=text, background="#FFFFE0", relief="solid", borderwidth=1, font=("Segoe UI", 9), padx=5, pady=2)
    label.pack()

    def enter(event):
        x = event.x_root + 10
        y = event.y_root + 5
        tooltip.geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

def create_gcode():
    """
    Generates a placeholder G-code block based on the selected tool
    and inserts it into the G-code text editor.
    """
    if gcode_text_widget is None or tool_selection_var is None or status_var is None:
        messagebox.showerror("Error", "UI elements not initialized for G-code creation.")
        return

    tool = tool_selection_var.get()
    sample = f"; -- Created block for {tool} --\nG1 X10 Y10 Z0.3\nG1 X20 Y20 Z0.3\n"
    gcode_text_widget.insert('end', '\n' + sample)
    status_var.set(f"Sample G-code for {tool} created.")

def save_gcode_file():
    """Saves the content of the G-code text area to a file."""
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text area not initialized.")
        return

    content = gcode_text_widget.get('1.0', 'end').strip()
    if not content:
        messagebox.showwarning("Warning", "No content to save.")
        status_var.set("Save cancelled: No content.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".gcode",
        filetypes=[("G-code files", "*.gcode"), ("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not file_path:
        status_var.set("Save cancelled by user.")
        return

    try:
        with open(file_path, 'w') as f:
            f.write(content)
        messagebox.showinfo("Success", f"File saved to:\n{file_path}")
        status_var.set(f"Saved: {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")
        status_var.set("Error saving file.")

def load_gcode_file():
    """Loads a G-code file into the G-code text area."""
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text area not initialized.")
        return

    gcode_text_widget.delete('1.0', 'end')
    filepath = filedialog.askopenfilename(
        filetypes=[("G-code or text files", "*.gcode *.txt"), ("All files", "*.*")]
    )
    if not filepath:
        status_var.set("Load cancelled by user.")
        return

    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
        gcode_text_widget.insert('1.0', ''.join(lines))
        messagebox.showinfo("Success", f"Loaded {len(lines)} lines from:\n{filepath}")
        status_var.set(f"Loaded: {os.path.basename(filepath)}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{e}")
        status_var.set("Error loading file.")

def parse_gcode():
    """Parses the G-code from the text area and displays X, Y, Z coordinates."""
    if gcode_text_widget is None or result_text_widget is None or status_var is None:
        messagebox.showerror("Error", "Text areas not initialized.")
        return

    lines = gcode_text_widget.get('1.0', 'end').strip().split('\n')
    if not any(line.strip() for line in lines):
        messagebox.showwarning("Warning", "No G-code loaded to parse.")
        status_var.set("Parsing cancelled: No G-code.")
        return

    results = []
    for i, line in enumerate(lines, 1):
        x = get_x(line)
        y = get_y(line)
        z = get_z(line)
        results.append(f"Line {i}: X={x if x is not None else 'N/A'}, Y={y if y is not None else 'N/A'}, Z={z if z is not None else 'N/A'}")

    result_text_widget.delete('1.0', 'end')
    if results:
        result_text_widget.insert('1.0', '\n'.join(results))
        status_var.set(f"Parsed {len(results)} coordinate lines.")
    else:
        result_text_widget.insert('1.0', "No G0/G1 movements with coordinates found.")
        status_var.set("Parsing complete: No movements found.")


def on_print_block():
    """
    Handles the "Print Block" button click, asks for a save location,
    calls the print_block logic function, and then loads the generated
    G-code back into the text widget.
    """
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized. Please ensure the UI is fully loaded before using this function.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode",
                                         filetypes=[("G-code files", "*.gcode"), ("All files", "*.*")])
    if not path:
        status_var.set("Print Block generation cancelled.")
        return

    try:
        mock_file = MockFile()

        z_value = 0.3
        g0_feed = "1500"
        g1_feed = "1200"
        square = True
        deposition = False
        x_value = 10.0
        y_value = 10.0
        vertical_lift = 0.5
        delay = 100
        step = False
        ultrasound = False
        next_angle = 90.0
        a_feed = 800

        new_ultrasound_state = print_block(
            destination=mock_file,
            z_value=z_value,
            g0_xy_feed=g0_feed,
            g1_xy_feed=g1_feed,
            square_button=square,
            deposition=deposition,
            x_value=x_value,
            y_value=y_value,
            vertical_lift=vertical_lift,
            delay_time=delay,
            step_button=step,
            ultrasound_state=ultrasound,
            z_feed=int(g0_feed),
            next_tool_angle=next_angle,
            a_feed=a_feed
        )

        gcode_content = mock_file.getvalue()

        with open(path, 'w') as f:
            f.write(gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', gcode_content)

        messagebox.showinfo("Success", f"Print Block G-code generated and saved to:\n{path}\nContent loaded into editor. Ultrasound state: {new_ultrasound_state}")
        status_var.set(f"Print Block G-code generated. Ultrasound: {new_ultrasound_state}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Print Block G-code:\n{e}")
        status_var.set("Error generating Print Block G-code.")

def on_clean_block():
    """
    Handles the "Clean Block" button click, generates G-code using clean_block logic,
    and loads it into the G-code text editor.
    """
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode")
    if not path:
        status_var.set("Clean Block generation cancelled.")
        return

    try:
        mock_file = MockFile()
        x_value = 0.0
        y_value = 0.0
        z_value = 0.3
        z_feed = 1000
        delay_time = 500
        clean_block(mock_file, x_value, y_value, z_value, z_feed, delay_time)

        gcode_content = mock_file.getvalue()
        with open(path, 'w') as f:
            f.write(gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', gcode_content)
        messagebox.showinfo("Success", f"Clean Block G-code generated and loaded.")
        status_var.set("Clean Block G-code generated.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Clean Block G-code:\n{e}")
        status_var.set("Error generating Clean Block G-code.")

def on_clean_no_tool_block():
    """
    Handles the "Clean No Tool Block" button click, generates G-code using
    clean_no_tool_block logic, and loads it into the G-code text editor.
    """
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode")
    if not path:
        status_var.set("Clean No Tool Block generation cancelled.")
        return

    try:
        mock_file = MockFile()
        x_value = 0.0
        y_value = 0.0
        z_value = 0.3
        z_feed = 800
        delay_time = 400
        clean_no_tool_block(mock_file, x_value, y_value, z_value, z_feed, delay_time)

        gcode_content = mock_file.getvalue()
        with open(path, 'w') as f:
            f.write(gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', gcode_content)
        messagebox.showinfo("Success", "Clean No Tool Block G-code generated and loaded.")
        status_var.set("Clean No Tool Block G-code generated.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Clean No Tool Block G-code:\n{e}")
        status_var.set("Error generating Clean No Tool Block G-code.")

def on_print_cylinder():
    """
    Handles the "Print Cylinder" button click, generates G-code using print_cylinder logic,
    and loads it into the G-code text editor.
    """
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode")
    if not path:
        status_var.set("Print Cylinder generation cancelled.")
        return

    try:
        mock_file = MockFile()
        x_center = 10.0
        y_center = 10.0
        z_value = 0.3
        radius = 5.0
        segments = 36
        feedrate = 1200
        print_cylinder(mock_file, x_center, y_center, z_value, radius, segments, feedrate)

        gcode_content = mock_file.getvalue()
        with open(path, 'w') as f:
            f.write(gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', gcode_content)
        messagebox.showinfo("Success", f"Print Cylinder G-code generated and loaded.")
        status_var.set("Print Cylinder G-code generated.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Print Cylinder G-code:\n{e}")
        status_var.set("Error generating Print Cylinder G-code.")

def on_print_layer0():
    """
    Handles the "Print Layer0" button click, generates G-code using
    print_layer0 logic, and loads it into the G-code text editor.
    """
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode")
    if not path:
        status_var.set("Print Layer0 generation cancelled.")
        return

    try:
        mock_file = MockFile()
        x_start = 0.0
        y_start = 0.0
        x_end = 20.0
        y_end = 0.0
        z_value = 0.3
        feedrate = 1000
        print_layer0(mock_file, x_start, y_start, x_end, y_end, z_value, feedrate)

        gcode_content = mock_file.getvalue()
        with open(path, 'w') as f:
            f.write(gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', gcode_content)
        messagebox.showinfo("Success", "Print Layer0 G-code generated and loaded.")
        status_var.set("Print Layer0 G-code generated.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Print Layer0 G-code:\n{e}")
        status_var.set("Error generating Print Layer0 G-code.")

def on_rotate():
    """
    Handles the "Rotate" button click, generates G-code using rotate logic,
    and loads it into the G-code text editor.
    """
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode")
    if not path:
        status_var.set("Rotate G-code generation cancelled.")
        return

    try:
        mock_file = MockFile()
        current_angle = 0
        rotate_by = 90
        x_value = 10.0
        y_value = 10.0
        z_value = 0.3
        feedrate = 1200
        new_angle = rotate(mock_file, current_angle, rotate_by, x_value, y_value, z_value, feedrate)

        gcode_content = mock_file.getvalue()
        with open(path, 'w') as f:
            f.write(gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', gcode_content)
        messagebox.showinfo("Success", f"Rotate G-code generated and loaded. New angle: {new_angle}")
        status_var.set(f"Rotate G-code generated. New angle: {new_angle}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Rotate G-code:\n{e}")
        status_var.set("Error generating Rotate G-code.")

def on_slicer():
    """
    Handles the "Slicer" button click, generates G-code using slicer logic,
    and loads it into the G-code text editor.
    """
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode")
    if not path:
        status_var.set("Slicer G-code generation cancelled.")
        return

    try:
        mock_file = MockFile()
        x_start = 0.0
        x_end = 20.0
        y_value = 10.0
        z_value = 0.3
        layers = 5
        feedrate = 1000
        slicer(mock_file, x_start, x_end, y_value, z_value, layers, feedrate)

        gcode_content = mock_file.getvalue()
        with open(path, 'w') as f:
            f.write(gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', gcode_content)
        messagebox.showinfo("Success", "Slicer G-code generated and loaded.")
        status_var.set("Slicer G-code generated.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Slicer G-code:\n{e}")
        status_var.set("Error generating Slicer G-code.")

def on_print_zigzag():
    """
    Handles the "Print ZigZag" button click, generates G-code using
    print_zigzag logic, and loads it into the G-code text editor.
    """
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode")
    if not path:
        status_var.set("Print ZigZag generation cancelled.")
        return

    try:
        mock_file = MockFile()
        x_start = 0.0
        x_end = 20.0
        y_value = 10.0
        z_value = 0.3
        passes = 10
        feedrate = 1000
        print_zigzag(mock_file, x_start, x_end, y_value, z_value, passes, feedrate)

        gcode_content = mock_file.getvalue()
        with open(path, 'w') as f:
            f.write(gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', gcode_content)
        messagebox.showinfo("Success", "Print ZigZag G-code generated and loaded.")
        status_var.set("Print ZigZag G-code generated.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Print ZigZag G-code:\n{e}")
        status_var.set("Error generating Print ZigZag G-code.")


def create_ui():
    """Creates and lays out the main UI elements of the application."""
    global gcode_text_widget, result_text_widget, tool_selection_var, status_var

    root = tk.Tk()
    root.title("Simplified3D G-code Converter")
    root.geometry("1400x750")
    root.configure(bg="#f8fafb")

    # ---- TOOL + BUTTONS ----
    control_frame = tk.LabelFrame(root, text="Controls", font=("Segoe UI", 11, "bold"), bg="#f8fafb", padx=12, pady=8)
    control_frame.pack(fill='x', padx=14, pady=(10, 2))

    tool_frame = tk.Frame(control_frame, bg="#f8fafb")
    tool_frame.pack(side='left', padx=(0, 14), pady=4)
    tk.Label(tool_frame, text="Tool:", font=("Segoe UI", 10), bg="#f8fafb").pack(side='left', padx=(0, 4))
    tool_selection_var = tk.StringVar(value="T0")
    tool_combo = ttk.Combobox(tool_frame, textvariable=tool_selection_var,
                              values=[f"T{i}" for i in range(10)], state="readonly", width=5)
    tool_combo.pack(side='left', padx=(4, 0))

    button_grid_frame = tk.Frame(control_frame, bg="#f8fafb")
    button_grid_frame.pack(side='left', fill='x', expand=True)

    def add_button(parent_frame, label, command, tip, row, col):
        btn = tk.Button(parent_frame, text=label, command=command,
                        font=("Segoe UI", 10, "bold"), bg="#2978b5", fg="white",
                        relief="groove", activebackground="#24577a", width=16, height=1)
        btn.grid(row=row, column=col, padx=4, pady=4, sticky="ew")
        show_tooltip(btn, tip)
        return btn

    add_button(button_grid_frame, "Load G-code File", load_gcode_file, "Open a G-code file into the editor", 0, 0)
    add_button(button_grid_frame, "Save G-code File", save_gcode_file, "Save current G-code editor contents", 0, 1)
    add_button(button_grid_frame, "Parse G-code", parse_gcode, "Show all X,Y,Z for loaded G-code", 0, 2)
    add_button(button_grid_frame, "Create G-code", create_gcode, "Insert a sample G-code block", 0, 3)

    add_button(button_grid_frame, "Print Block", on_print_block, "Generate Print Block G-code", 1, 0)
    add_button(button_grid_frame, "Clean Block", on_clean_block, "Generate Clean Block G-code", 1, 1)
    add_button(button_grid_frame, "Clean No Tool Block", on_clean_no_tool_block, "Generate Clean No Tool Block G-code", 1, 2)
    add_button(button_grid_frame, "Print Cylinder", on_print_cylinder, "Generate Print Cylinder G-code", 1, 3)

    add_button(button_grid_frame, "Print Layer0", on_print_layer0, "Generate Layer0 G-code", 2, 0)
    add_button(button_grid_frame, "Rotate", on_rotate, "Rotate tool position and emit G-code", 2, 1)
    add_button(button_grid_frame, "Slicer", on_slicer, "Run slicer and emit G-code", 2, 2)
    add_button(button_grid_frame, "Print ZigZag", on_print_zigzag, "Generate ZigZag pattern G-code", 2, 3)

    for i in range(4):
        button_grid_frame.grid_columnconfigure(i, weight=1)


    # ---- G-code Editor Area ----
    gcode_frame = tk.LabelFrame(root, text="G-code Editor", font=("Segoe UI", 11, "bold"), bg="#f8fafb")
    gcode_frame.pack(fill='both', expand=True, padx=14, pady=(8, 3))

    text_frame = tk.Frame(gcode_frame, bg="#f8fafb")
    text_frame.pack(fill='both', expand=True, padx=6, pady=8)
    gcode_text_widget = Text(text_frame, wrap='none', height=14,
                             bg="#e7f1fb", fg="#252525", font=("Consolas", 11), relief="flat", bd=2)
    gcode_text_widget.pack(side='left', fill='both', expand=True)
    scrollbar = Scrollbar(text_frame, command=gcode_text_widget.yview)
    scrollbar.pack(side='right', fill='y')
    gcode_text_widget.config(yscrollcommand=scrollbar.set)

    # ---- Results Area ----
    result_frame = tk.LabelFrame(root, text="Parsed (X, Y, Z) Results", font=("Segoe UI", 11, "bold"), bg="#f8fafb")
    result_frame.pack(fill='both', expand=True, padx=14, pady=(3, 10))
    results_text_frame = tk.Frame(result_frame, bg="#f8fafb")
    results_text_frame.pack(fill='both', expand=True, padx=6, pady=6)
    result_text_widget = Text(results_text_frame, wrap='none', height=7,
                              bg="#eaf7f4", fg="#222", font=("Consolas", 11), relief="flat", bd=2)
    result_text_widget.pack(side='left', fill='both', expand=True)
    result_scrollbar = Scrollbar(results_text_frame, command=result_text_widget.yview)
    result_scrollbar.pack(side='right', fill='y')
    result_text_widget.config(yscrollcommand=result_scrollbar.set)

    # ---- Status Bar ----
    status_var = tk.StringVar(value="Ready")
    status = tk.Label(root, textvariable=status_var, bd=1, relief='sunken', anchor='w',
                      font=("Segoe UI", 9), bg="#e8e8e8", padx=5)
    status.pack(fill='x', side='bottom')

    root.mainloop()

if __name__ == "__main__":
    gcode_text_widget = None
    result_text_widget = None
    tool_selection_var = None
    status_var = None
    create_ui()
    