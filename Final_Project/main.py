import tkinter as tk
import time
import winsound
import os


# This list would be where the timer is from and if the timer is currently couting
# I used list so that it can be modfieid by functions
values = [        
                  1500, # Timer
                  True, # Can start Timer
                  None, # stores current running timer
                  1, # Task number
        ]

def change_display_timer():
        display_time = format_time_display(values[0])
        timer_label.config(text=display_time)

        #print(display_time)

def format_time_display(seconds):
    """
    Converts total seconds into 'mm:ss' string format for the active countdown display.
    """
    # Calculate minutes and remaining seconds
    mins, secs = divmod(seconds, 60)
    
    # Ensures two digits for minutes and seconds
    return f"{mins:02}:{secs:02}"


def start_timer_controller():
    if timer_button["text"]== "START":
        values[1] = True
        if values[2] == None:
            start_timer()
        timer_button.config(text="PAUSE")

    elif timer_button["text"] == "PAUSE":
        timer_button.config(text="START")
        values[1] = True
        root.after_cancel(values[2])
        values[2] = None
        values[0] += 1
        print(values)


def start_timer():
    """Runs the countdown timer."""

    print(values)
    if values[0] >= 0 and values[1]: # only starts if timer is not 0 and if it can startvalues[2]
        
        change_display_timer()
        values[2] = root.after(1000, start_timer) # stores current timer 
        values[0] -= 1


def pomodoro_timer():
    values[0] = 1500

    values[1] = False
    if values[2] != None:
        root.after_cancel(values[2])
        values[2] = None
    change_display_timer()
    timer_button.config(text="START")
    print(values)

def short_timer():
    values[0] = 300
    values[1] = False
    if values[2] != None:
        root.after_cancel(values[2])
        values[2] = None
    change_display_timer()
    timer_button.config(text="START")
    print(values)

def long_timer():
    values[0] = 900
    values[1] = False
    if values[2] != None:
        root.after_cancel(values[2])
        values[2] = None
    change_display_timer()
    timer_button.config(text="START")
    print(values)

def delete_button(event):
    event.widget.destroy()
    values[3] -= 1

def add_new_task():
    new_task = tk.Button(scrollable_frame, text=f"Item {values[3]}", font=("Arial", 12), bg="white", anchor="nw")
    new_task.propagate(False)
    new_task.bind("<Button-1>", delete_button)
    new_task.grid(row=values[3], column=0, sticky="ew", padx=5, pady=2)  # Use sticky="ew"
    values[3] += 1

def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


root = tk.Tk()

root.geometry("750x500")
root.config(bg="red")
root.maxsize(750, 500)

# left frames
left_frame = tk.Frame(root, bg="purple", height=500, width=500)
top_frame = tk.Frame(left_frame, bg="red", height=100, width=500)
hero_frame = tk.Frame(left_frame, bg="orange", height=200, width=500)
button_frame = tk.Frame(left_frame, bg="red", height=100, width=500)
bottom_frame = tk.Frame(left_frame, bg="red", height=100, width=500)

# timer
timer_label = tk.Label(hero_frame, bg="orange", text="25:00", font=("Regular", 64))
timer_button = tk.Button(hero_frame, bg="white", text="START", font=("Regular", 26), command=start_timer_controller)

# buttons
pomodoro_button = tk.Button(button_frame, bg="white", text="Pomodoro", font=("Regular", 20), command=pomodoro_timer)
short_button = tk.Button(button_frame, bg="white", text="Short-break", font=("Regular", 20), command=short_timer)
long_button = tk.Button(button_frame, bg="white", text="Long-break", font=("Regular", 20), command=long_timer)

# so that frames doesnt automatically shrink to its children
left_frame.grid_propagate(False)
top_frame.grid_propagate(False)
hero_frame.grid_propagate(False)
button_frame.grid_propagate(False)
bottom_frame.grid_propagate(False)

# so that frames expands on all direction within its space
left_frame.grid(row=0, column=0, sticky="nsew")
top_frame.grid(row=0, sticky="nsew")
hero_frame.grid(row=1, sticky="nsew")
button_frame.grid(row=3, sticky="nsew")
bottom_frame.grid(row=4, sticky="nsew")


#
hero_frame.rowconfigure(0, weight=2)
hero_frame.rowconfigure(1, weight=1)

#
hero_frame.columnconfigure(0, weight=1)

#
timer_label.grid(row=0,  sticky="nsew")
timer_button.grid(row=1)

# so that the buttons in button_frame have the same sizes and vertically resizes
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

# so that buttons horizontally resizes
button_frame.rowconfigure(0, weight=1)

# so that buttons expands to fill out all directons wihtin its space
pomodoro_button.grid(row=0, column=0, sticky="nsew")
short_button.grid(row=0, column=1, sticky="nsew")
long_button.grid(row=0, column=2, sticky="nsew")

#
left_frame.rowconfigure(0, weight=1)
left_frame.rowconfigure(1, weight=2)
left_frame.rowconfigure(2, weight=1)
left_frame.rowconfigure(3, weight=1)

#
left_frame.columnconfigure(0, weight=1)

""" Right Side of the Program """

# right frames
right_frame = tk.Frame(root, bg="blue", height= 500, width=250)
right_frame.propagate(False)
right_frame.grid(row=0, column=1, sticky="nsew")

to_do_list_title = tk.Label(right_frame,text="To Do List", font=("Regular", 24))
to_do_list_title.grid(row=0, column=0, columnspan=2, sticky="nsew")

add_task_button = tk.Button(right_frame, text="Add New Task", font=("Regular", 18), command=add_new_task)
add_task_button.grid(row=1, column=0, columnspan=2, sticky="nsew")

canvas = tk.Canvas(right_frame, bg="white", width=230, height=400)

canvas.grid(row=2, column=0, sticky="nsew")
canvas.rowconfigure(0, weight=1)
canvas.columnconfigure(0, weight=1)

scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=2, column=1, sticky="nsew")

canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas, bg="white", )
scrollable_frame.columnconfigure(0, weight=1)
scrollable_frame.propagate(False)
scrollable_frame.bind("<Configure>", update_scrollregion)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())


scrollable_frame.grid_columnconfigure(0, weight=1)

right_frame.columnconfigure(0, weight=1)
right_frame.columnconfigure(1, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_rowconfigure(2, weight=1)

""" All """
#
root.grid_rowconfigure(0, weight=1)

# so that frames resizes vertically
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)



root.mainloop()