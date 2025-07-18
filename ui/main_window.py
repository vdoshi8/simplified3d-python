import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar, ttk
from typing import Optional, Union, Tuple
import re
import io

# Set up the project root for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import real logic functions from the 'logic' directory
from logic.print_block import print_block
from logic.geometry import get_x, get_y, get_z
from logic.clean_block import clean_block
from logic.clean_no_tool_block import clean_no_tool_block
from logic.print_cylinder import print_cylinder
from logic.print_layer0 import print_layer0
from logic.rotate import rotate
from logic.slicer import slicer
from logic.print_zigzag import print_zigzag


# Global variables to hold the Text widgets and StringVar for tool selection
gcode_text_widget: Optional[Text] = None
result_text_widget: Optional[Text] = None
tool_selection_var: Optional[tk.StringVar] = None
status_var: Optional[tk.StringVar] = None
waveform_option: Optional[tk.StringVar] = None

def replace_m3_m5(gcode: str) -> str:
    """
    Replaces M3 with M98 P"us.g" and comments out M5 lines in the G-code string.
    """
    lines = []
    for line in gcode.splitlines():
        if re.match(r'^\s*M3(\s*;.*)?$', line):
            lines.append('M98 P"us.g"')
        elif re.match(r'^\s*M5(\s*;.*)?$', line):
            lines.append(';M5')
        else:
            lines.append(line)
    return "\n".join(lines)


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
    if gcode_text_widget is None or tool_selection_var is None or status_var is None or waveform_option is None:
        messagebox.showerror("Error", "UI elements not initialized for G-code creation.")
        return

    tool = tool_selection_var.get()
    waveform = waveform_option.get()
    sample = f"; -- Created block for {tool} with {waveform} waveform --\nG1 X10 Y10 Z0.3\nM3\nG1 X20 Y20 Z0.3\nM5\nG1 X30 Y30 Z0.3\n"
    processed_sample = replace_m3_m5(sample)
    gcode_text_widget.insert('end', '\n' + processed_sample)
    status_var.set(f"Sample G-code for {tool} ({waveform}) created and processed.")


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
        processed_content = replace_m3_m5(content)
        with open(file_path, 'w') as f:
            f.write(processed_content)
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
            content = f.read()
        processed_content = replace_m3_m5(content)
        gcode_text_widget.insert('1.0', processed_content)
        messagebox.showinfo("Success", f"Loaded {len(processed_content.splitlines())} lines from:\n{filepath}")
        status_var.set(f"Loaded: {os.path.basename(filepath)}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{e}")
        status_var.set("Error loading file.")

def clear_editor():
    """Clears the content of the G-code editor text widget."""
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code editor not initialized.")
        return
    gcode_text_widget.delete('1.0', 'end')
    status_var.set("G-code editor cleared.")

def clear_results():
    """Clears the content of the parsed results text widget."""
    if result_text_widget is None or status_var is None:
        messagebox.showerror("Error", "Results display not initialized.")
        return
    result_text_widget.delete('1.0', 'end')
    status_var.set("Parsed results cleared.")

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
    else:
        result_text_widget.insert('1.0', "No G0/G1 movements with coordinates found.")
    status_var.set("Parsing complete: No movements found.")


def on_print_block():
    """
    Handles the "Print Block" button click, asks for a save location,
    calls the print_block logic function, and then loads the generated
    G-code back into the text widget.
    """
    if gcode_text_widget is None or status_var is None or waveform_option is None:
        messagebox.showerror("Error", "UI elements not initialized. Please ensure the UI is fully loaded before using this function.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode",
                                         filetypes=[("G-code files", "*.gcode"), ("All files", "*.*")])
    if not path:
        status_var.set("Print Block generation cancelled.")
        return

    try:
        z_value = 0.3
        g0_feed = "1500"
        g1_feed = "1200"
        deposition = False
        x_value = 10.0
        y_value = 10.0
        vertical_lift = 0.5
        delay = 100
        step = False
        ultrasound = False
        next_angle = 90.0
        a_feed = 800
        waveform = waveform_option.get()

        temp_gcode_buffer = io.StringIO()

        new_ultrasound_state = print_block(
            destination=temp_gcode_buffer,
            z_value=z_value,
            g0_xy_feed=g0_feed,
            g1_xy_feed=g1_feed,
            deposition=deposition,
            x_value=x_value,
            y_value=y_value,
            vertical_lift=vertical_lift,
            delay_time=delay,
            step_button=step,
            ultrasound_state=ultrasound,
            z_feed=int(g0_feed),
            next_tool_angle=next_angle,
            a_feed=a_feed,
            waveform=waveform
        )

        gcode_content = temp_gcode_buffer.getvalue()
        processed_gcode_content = replace_m3_m5(gcode_content)

        with open(path, 'w') as f:
            f.write(processed_gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', processed_gcode_content)

        messagebox.showinfo("Success", f"Print Block G-code generated and saved to:\n{path}\nContent loaded into editor. Ultrasound state: {new_ultrasound_state}")
        status_var.set(f"Print Block G-code generated. Ultrasound: {new_ultrasound_state}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Print Block G-code:\n{e}")
        status_var.set("Error generating Print Block G-code.")


def on_clean_block():
    """
    Handles the "Clean Block" button click, generates G-code using
    clean_block logic, and loads it into the G-code text editor.
    """
    if gcode_text_widget is None or status_var is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode", filetypes=[("G-code Files", "*.gcode"), ("All Files", "*.*")])
    if not path:
        status_var.set("Clean Block G-code generation cancelled.")
        return

    try:
        temp_gcode_buffer = io.StringIO()

        x_value = 0.0
        y_value = 0.0
        z_value = 0.3
        g0_xy_feed = 5000
        g1_xy_feed = 1000
        delay_time = 0.1
        
        clean_block(
            temp_gcode_buffer,
            x_value,
            y_value,
            z_value,
            g0_xy_feed,
            g1_xy_feed,
            delay_time
        ) 

        gcode_content = temp_gcode_buffer.getvalue()
        processed_gcode_content = replace_m3_m5(gcode_content)

        with open(path, 'w') as f:
            f.write(processed_gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', processed_gcode_content)
        messagebox.showinfo("Success", "Clean Block G-code generated and loaded.")
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
        temp_gcode_buffer = io.StringIO()

        x_value = 0.0
        y_value = 0.0
        z_value = 0.3
        z_feed = 800
        delay_time = 400

        clean_no_tool_block(temp_gcode_buffer, x_value, y_value, z_value, z_feed, delay_time)

        gcode_content = temp_gcode_buffer.getvalue()
        processed_gcode_content = replace_m3_m5(gcode_content)

        with open(path, 'w') as f:
            f.write(processed_gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', processed_gcode_content)
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
        temp_gcode_buffer = io.StringIO()

        x_center = 10.0
        y_center = 10.0
        z_value = 0.3
        radius = 5.0
        segments = 36
        feedrate = 1200

        print_cylinder(temp_gcode_buffer, x_center, y_center, z_value, radius, segments, feedrate)

        gcode_content = temp_gcode_buffer.getvalue()
        processed_gcode_content = replace_m3_m5(gcode_content)

        with open(path, 'w') as f:
            f.write(processed_gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', processed_gcode_content)
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
        temp_gcode_buffer = io.StringIO()

        x_start = 0.0
        y_start = 0.0
        x_end = 20.0
        y_end = 0.0
        z_value = 0.3
        feedrate = 1000

        print_layer0(temp_gcode_buffer, x_start, y_start, x_end, y_end, z_value, feedrate)

        gcode_content = temp_gcode_buffer.getvalue()
        processed_gcode_content = replace_m3_m5(gcode_content)

        with open(path, 'w') as f:
            f.write(processed_gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', processed_gcode_content)
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
        temp_gcode_buffer = io.StringIO()

        current_angle = 0
        rotate_by = 90
        x_value = 10.0
        y_value = 10.0
        z_value = 0.3
        feedrate = 1200

        new_angle = rotate(temp_gcode_buffer, current_angle, rotate_by, x_value, y_value, z_value, feedrate)

        gcode_content = temp_gcode_buffer.getvalue()
        processed_gcode_content = replace_m3_m5(gcode_content)

        with open(path, 'w') as f:
            f.write(processed_gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', processed_gcode_content)
        messagebox.showinfo("Success", f"Rotate G-code generated and loaded. New angle: {new_angle}")
        status_var.set(f"Rotate G-code generated. New angle: {new_angle}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Rotate G-code:\n{e}")
        status_var.set("Error generating Rotate G-code.")

def on_slicer():
    global gcode_text_widget, status_var, waveform_option

    if gcode_text_widget is None or status_var is None or waveform_option is None:
        messagebox.showerror("Error", "G-code text editor or status bar is not initialized.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".gcode")
    if not path:
        status_var.set("Slicer G-code generation cancelled.")
        return

    try:
        temp_gcode_buffer = io.StringIO()

        x_min_val = 0.0
        x_max_val = 20.0
        y_min_val = 0.0
        y_max_val = 20.0
        
        z_height = 1.5
        fill_density = 0.8
        layer_thickness = 0.3
        nozzle_diameter = 0.4
        g0_feed = 5000
        g1_feed = 1000
        waveform = waveform_option.get()

        slicer(
            destination=temp_gcode_buffer,
            z_height=z_height,
            fill_density=fill_density,
            layer_thickness=layer_thickness,
            nozzle_diameter=nozzle_diameter,
            g0_feed=g0_feed,
            g1_feed=g1_feed,
            x_min=x_min_val,
            x_max=x_max_val,
            y_min=y_min_val,
            y_max=y_max_val,
            waveform=waveform
        )

        gcode_content = temp_gcode_buffer.getvalue()
        processed_gcode_content = replace_m3_m5(gcode_content)

        with open(path, 'w') as f:
            f.write(processed_gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', processed_gcode_content)
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
        temp_gcode_buffer = io.StringIO()

        x_start = 0.0
        x_end = 20.0
        y_value = 10.0
        z_value = 0.3
        passes = 10
        feedrate = 1000

        print_zigzag(temp_gcode_buffer, x_start, x_end, y_value, z_value, passes, feedrate)

        gcode_content = temp_gcode_buffer.getvalue()
        processed_gcode_content = replace_m3_m5(gcode_content)

        with open(path, 'w') as f:
            f.write(processed_gcode_content)

        gcode_text_widget.delete('1.0', 'end')
        gcode_text_widget.insert('1.0', processed_gcode_content)
        messagebox.showinfo("Success", "Print ZigZag G-code generated and loaded.")
        status_var.set("Print ZigZag G-code generated.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate/save Print ZigZag G-code:\n{e}")
        status_var.set("Error generating Print ZigZag G-code.")

def on_convert_gcode():
    if status_var is None or waveform_option is None:
        messagebox.showerror("Error", "UI not fully initialized.")
        return

    input_path = filedialog.askopenfilename(
        filetypes=[("G-code files", "*.gcode *.txt"), ("All files", "*.*")]
    )
    if not input_path:
        status_var.set("Conversion cancelled: no input file.")
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".gcode",
        filetypes=[("G-code files", "*.gcode"), ("All files", "*.*")]
    )
    if not output_path:
        status_var.set("Conversion cancelled: no output file.")
        return

    waveform = waveform_option.get()

    try:
        with open(input_path, "r") as infile, open(output_path, "w") as outfile:
            outfile.write(f"; Converted with {waveform} waveform\n")
            for line in infile:
                line = re.sub(r"^\s*M3(\s*;.*)?$", 'M98 P"us.g"\n', line)
                line = re.sub(r"^\s*M5(\s*;.*)?$", ';M5\n', line)
                outfile.write(line)

        messagebox.showinfo("Success", f"Converted G-code written to:\n{output_path}")
        status_var.set("Conversion completed successfully.")

        if gcode_text_widget is not None:
            with open(output_path, "r") as f:
                gcode_text_widget.delete('1.0', 'end')
                gcode_text_widget.insert('1.0', f.read())

    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n{e}")
        status_var.set("Conversion failed.")


def create_ui():
    """Creates and lays out the main UI elements of the application."""
    global gcode_text_widget, result_text_widget, tool_selection_var, status_var, waveform_option

    root = tk.Tk()
    root.title("Simplified3D G-code Converter")
    root.geometry("1100x600")
    root.minsize(900, 550)
    root.configure(bg="#f8fafb")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    controls_panel = tk.Frame(main_frame, bg="#eaeaea", width=210)
    controls_panel.pack(side="left", fill="y", padx=10, pady=10)
    controls_panel.pack_propagate(False)

    def add_button(parent_frame, label, command, tip, pady_val: Union[int, Tuple[int, int]] = 2):
        btn = tk.Button(parent_frame, text=label, command=command,
                        font=("Segoe UI", 10, "bold"), bg="#2978b5", fg="white",
                        relief="groove", activebackground="#24577a", width=20)
        btn.pack(fill="x", padx=5, pady=pady_val)
        show_tooltip(btn, tip)
        return btn

    ttk.Label(controls_panel, text="Tool:", font=("Segoe UI", 10, "bold"), background="#eaeaea").pack(anchor="w", padx=5, pady=(0, 2))
    tool_selection_var = tk.StringVar(value="T0")
    tool_combo = ttk.Combobox(controls_panel, textvariable=tool_selection_var,
                              values=[f"T{i}" for i in range(10)], width=10, state="readonly")
    tool_combo.pack(anchor="w", padx=5, pady=(0,10))

    waveform_option = tk.StringVar(value="sawtooth")
    waveform_frame = tk.LabelFrame(controls_panel, text="Waveform", font=("Segoe UI", 10, "bold"), bg="#eaeaea")
    waveform_frame.pack(anchor="w", fill="x", padx=5, pady=(5,10))
    tk.Radiobutton(waveform_frame, text="Saw-tooth", variable=waveform_option, value="sawtooth", bg="#eaeaea").pack(anchor="w")
    tk.Radiobutton(waveform_frame, text="Square wave", variable=waveform_option, value="square", bg="#eaeaea").pack(anchor="w")

    add_button(controls_panel, "Load G-code File", load_gcode_file, "Open a G-code file into the editor")
    add_button(controls_panel, "Save G-code File", save_gcode_file, "Save current G-code editor contents")
    add_button(controls_panel, "Clear Editor", clear_editor, "Clear all text from the G-code editor", pady_val=(2,10))
    add_button(controls_panel, "Convert G-code", on_convert_gcode, "Convert input file to output file using selected waveform")

    add_button(controls_panel, "Create G-code", create_gcode, "Insert a sample G-code block")
    add_button(controls_panel, "Parse G-code", parse_gcode, "Show all X,Y,Z for loaded G-code")
    add_button(controls_panel, "Clear Results", clear_results, "Clear all text from the results display", pady_val=(2,10))

    ttk.Label(controls_panel, text="Operations:", font=("Segoe UI", 10, "bold"), background="#eaeaea").pack(anchor="w", padx=5, pady=(12,2))
    add_button(controls_panel, "Print Block", on_print_block, "Generate Print Block G-code", pady_val=1)
    add_button(controls_panel, "Print Cylinder", on_print_cylinder, "Generate Print Cylinder G-code", pady_val=1)
    add_button(controls_panel, "Print ZigZag", on_print_zigzag, "Generate ZigZag pattern G-code", pady_val=1)
    add_button(controls_panel, "Clean Block", on_clean_block, "Generate Clean Block G-code", pady_val=1)
    add_button(controls_panel, "Clean No Tool Block", on_clean_no_tool_block, "Generate Clean No Tool Block G-code", pady_val=1)
    add_button(controls_panel, "Print Layer0", on_print_layer0, "Generate Layer0 G-code", pady_val=1)
    add_button(controls_panel, "Rotate", on_rotate, "Rotate tool position and emit G-code", pady_val=1)
    add_button(controls_panel, "Slicer", on_slicer, "Run slicer and emit G-code", pady_val=1)

    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="left", fill="both", expand=True, padx=(5,10), pady=10)

    tk.Label(right_frame, text="G-code Editor", font=("Segoe UI", 11, "bold"), bg="#f8fafb").pack(anchor="w")
    editor_frame = tk.Frame(right_frame, bg="#f4f8ff")
    editor_frame.pack(fill="both", expand=True, pady=(0,7))
    gcode_text_widget = Text(editor_frame, wrap='none', height=15,
                             bg="#eaf2fb", fg="#252525", font=("Consolas", 10), relief="flat", bd=2)
    gcode_text_widget.pack(side="left", fill="both", expand=True)
    scrollbar_editor = Scrollbar(editor_frame, command=gcode_text_widget.yview)
    scrollbar_editor.pack(side="right", fill="y")
    gcode_text_widget.config(yscrollcommand=scrollbar_editor.set)

    tk.Label(right_frame, text="Parsed (X, Y, Z) Results", font=("Segoe UI", 11, "bold"), bg="#f8fafb").pack(anchor="w", pady=(6,0))
    result_frame = tk.Frame(right_frame, bg="#f8fff8")
    result_frame.pack(fill="both", expand=True)
    result_text_widget = Text(result_frame, height=7, bg="#edfff0", font=("Consolas", 10), relief="flat", bd=2)
    result_text_widget.pack(side="left", fill="both", expand=True)
    scrollbar_results = Scrollbar(result_frame, command=result_text_widget.yview)
    scrollbar_results.pack(side="right", fill="y")
    result_text_widget.config(yscrollcommand=scrollbar_results.set)

    status_var = tk.StringVar(value="Ready")
    status_bar = tk.Label(root, textvariable=status_var, bd=1, relief="sunken", anchor="w", bg="#e8e8e8", padx=5)
    status_bar.pack(side="bottom", fill="x")

    root.mainloop()

if __name__ == "__main__":
    gcode_text_widget = None
    result_text_widget = None
    tool_selection_var = None
    status_var = None
    waveform_option = None
    create_ui()