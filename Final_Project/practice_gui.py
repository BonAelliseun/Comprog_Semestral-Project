import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x400")
root.title("Scrollable Frame Example")

     
# --- Create Canvas + Scrollbar ---
main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(main_frame, bg="black")
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.columnconfigure(0, weight=1)

# --- Scrollable Frame ---
scrollable_frame = tk.Frame(canvas)

# Bind the frame size to update scrollregion
def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", update_scrollregion)

# Add the frame to the canvas window
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# --- Add sample content ---
for i in range(50):
    tk.Label(scrollable_frame, text=f"Item {i+1}", font=("Arial", 12)).pack(anchor="w", pady=2)

root.mainloop()
