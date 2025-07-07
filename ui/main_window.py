import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar

# Import geometry parsing helpers from your logic module
from logic.geometry import get_x, get_y, get_z

def create_ui():
    root = tk.Tk()
    root.title("Simplified3D G-code Converter")

    # --- Button Frame ---
    button_frame = tk.Frame(root, padx=10, pady=10)
    button_frame.pack(side='top', fill='x')

    # --- G-code Text Area Frame (top) ---
    text_frame = tk.Frame(root)
    text_frame.pack(fill='both', expand=True, padx=10, pady=(5, 2))

    gcode_text = Text(text_frame, wrap='none', height=14, width=80,
                      bg="#f0f0f0", fg="#333333", font=("Consolas", 10))
    gcode_text.pack(side='left', fill='both', expand=True)
    scrollbar = Scrollbar(text_frame, command=gcode_text.yview)
    scrollbar.pack(side='right', fill='y')
    gcode_text.config(yscrollcommand=scrollbar.set)
    
    # --- Parsed Results Area (bottom) ---
    result_label = tk.Label(root, text="Parsed (X, Y, Z) Results:", anchor='w')
    result_label.pack(fill='x', padx=12, pady=(8,0))

    result_frame = tk.Frame(root)
    result_frame.pack(fill='both', expand=True, padx=10, pady=(2,10))

    result_text = Text(result_frame, wrap='none', height=7, width=80,
                       bg="#eaf7f4", fg="#222", font=("Consolas", 10))
    result_text.pack(side='left', fill='both', expand=True)
    result_scrollbar = Scrollbar(result_frame, command=result_text.yview)
    result_scrollbar.pack(side='right', fill='y')
    result_text.config(yscrollcommand=result_scrollbar.set)

    # --- Functions ---
    def load_gcode_file():
        filepath = filedialog.askopenfilename(
            filetypes=[("G-code or text files", "*.gcode *.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return  # User cancelled
        try:
            with open(filepath, "r") as f:
                gcode_lines = f.readlines()
            gcode_text.delete('1.0', 'end')
            gcode_text.insert('1.0', ''.join(gcode_lines))
            messagebox.showinfo("Success", f"Loaded {len(gcode_lines)} lines from:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def parse_gcode():
        lines = gcode_text.get('1.0', 'end').strip().split('\n')
        if not lines or (len(lines) == 1 and lines[0] == ''):
            messagebox.showwarning("Warning", "No G-code loaded to parse.")
            return
        results = []
        for i, line in enumerate(lines, 1):
            x = get_x(line)
            y = get_y(line)
            z = get_z(line)
            results.append(f"Line {i}: X={x}, Y={y}, Z={z}")
        result_text.delete('1.0', 'end')
        result_text.insert('1.0', '\n'.join(results))

    # --- Buttons ---
    load_button = tk.Button(button_frame, text="Load G-code File", command=load_gcode_file)
    load_button.pack(side='left', padx=5, pady=5)

    parse_button = tk.Button(button_frame, text="Parse G-code", command=parse_gcode)
    parse_button.pack(side='left', padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
