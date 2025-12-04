import tkinter as tk
from pygame import mixer
import os


# This list would be where the timer is from and if the timer is currently couting=
# I used list so that it can be modfieid by functions
values = {
        "timer": 1500,
        "can_run": True,
        "cur_timer": None,
        "task_number": 1,
        "pomodoro_count": 0,
        "timer_tpye": "pomodoro"
}        

def play_bg_sound():
    path = os.path.dirname(__file__)
    path = os.path.join(path, "sounds", "bg.ogg")
    mixer.music.load(f"{path}")
    mixer.music.play(-1)

def load_sounds(music_name):
    path = os.getcwd()
    return mixer.sound(f"{path}\sounds\{music_name}")

def change_display_timer():
        display_time = format_time_display(values["timer"])
        timer_label.config(text=display_time)

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
        values["can_run"] = True
        if values["cur_timer"] == None:
            start_timer()
        timer_button.config(text="PAUSE")

    elif timer_button["text"] == "PAUSE":
        timer_button.config(text="START")
        values["can_turn"] = True
        root.after_cancel(values["cur_timer"])
        values["cur_timer"] = None
        values["timer"] += 1

def start_timer():
    """Runs the countdown timer."""
    if values["timer"] >= 0 and values["can_run"]: # only starts if timer is not 0 and if it can startvalues[2]
        change_display_timer()
        values["cur_timer"] = root.after(1000, start_timer) # stores current timer 
        values["timer"] -= 1
    elif values["timer"] <= 0 and values["can_run"]:
        if values["timer_tpye"] == "pomodoro":
            values["pomodoro_count"] += 1
        pomodoro_counter.config(text=values["pomodoro_count"])
        timer_button.config(text="START")
        
        if values["timer_tpye"] == "pomodoro" and values["pomodoro_count"] % 4 == 0:
            set_timer(4, "long-break")
        elif values["timer_tpye"] == "short-break" or values["timer_tpye"] == "long-break":
            set_timer(5, "pomodoro")
        else:
            set_timer(3, "short-break")
 

def set_timer(seconds, type):
    values["timer_tpye"] = type

    values["timer"] = seconds
    values["can_run"] = False
    if values["cur_timer"] != None:
        root.after_cancel(values["cur_timer"])
        values["cur_timer"] = None
    change_display_timer()
    timer_button.config(text="START")

def update_task(button_content):
    button_content["state"] = tk.DISABLED
    def edit_text(event):
        def edit():
            if len(task_name.get()) > 0:
                button_content.config(text=task_name.get())
            button_content["state"] = tk.DISABLED
            edit_text_window.destroy()
            button_content["state"] = tk.NORMAL

        update_window.destroy()
        edit_text_window = tk.Toplevel(root) 
        edit_text_window.title("New Window")
        edit_text_window.geometry("200x200") 
        edit_text_window.maxsize(200, 200)
        edit_text_window.minsize(200, 200)
        edit_text_window.columnconfigure(0, weight=1)
        edit_text_window.columnconfigure(1, weight=1) 
        edit_text_window.protocol("WM_DELETE_WINDOW", lambda: enable_button(button_content, edit_text_window))

        task_name = tk.Entry(edit_text_window, width=edit_text_window.winfo_reqwidth())
        task_name.grid(row= 0, column=0, sticky="nsew")

        done_button = tk.Button(edit_text_window, text="DONE", bg="red", font=("Regular", 16), command=edit)
        done_button.grid(row= 1, column=0, sticky="nsew")
        
    def done(event):
        update_window.destroy()
        button_content.destroy()
        values["task_number"] -= 1
        
    update_window = tk.Toplevel(root) 
    update_window.title("New Window")
    update_window.geometry("200x100") 
    update_window.maxsize(200, 100)
    update_window.minsize(200, 100)
    update_window.columnconfigure(0, weight=1)
    update_window.columnconfigure(1, weight=1)
    update_window.protocol("WM_DELETE_WINDOW", lambda: enable_button(button_content, update_window))

    edit_button = tk.Button(update_window, text="Edit", font=("Regular", 16))
    done_button = tk.Button(update_window, text="done", font=("Regular", 16))

    edit_button.grid(row=0, column=0, sticky="nsew")
    done_button.grid(row=0, column=1, sticky="nsew")

    edit_button.bind("<Button-1>", edit_text)
    done_button.bind("<Button-1>", done)

def enable_button(button, window):
    button["state"] = tk.NORMAL
    window.destroy()

def add_task_text(task_name, window=None):
    if len(task_name) > 0:      
        new_task = tk.Button(scrollable_frame, text=task_name, font=("Arial", 12), bg="white", anchor="nw", command=lambda: update_task(new_task))
        new_task.propagate(False)
        new_task.grid(row=values["task_number"], column=0, sticky="ew", padx=5, pady=2)  
        values["task_number"] += 1
    add_task_button["state"] = tk.NORMAL

    if window != None:
        window.destroy()

def save_tasks():
    tasks = scrollable_frame.winfo_children()

    with open("tasks.txt", "w") as f:
        for i in tasks:
            if i["text"].rfind("\n") == -1:
                f.write(i["text"] + "\n")
            else:
                f.write(i["text"])
        f.close()

def retreive_tasks():
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
        for i in tasks:
            add_task_text(i)
    f.close()

def add_new_task():
    add_task_button["state"] = tk.DISABLED

    new_window = tk.Toplevel(root)  # Create a new window
    new_window.title("New Window")
    new_window.geometry("250x150") 
    new_window.maxsize(250, 150)
    new_window.columnconfigure(0, weight=1)
    new_window.rowconfigure(0, weight=1)
    new_window.rowconfigure(1, weight=2)
    new_window.protocol("WM_DELETE_WINDOW", lambda: enable_button(add_task_button, new_window))

    task_name = tk.Entry(new_window, width=new_window.winfo_reqwidth())
    task_name.grid(row= 0, column=0, sticky="nsew")

    done_button = tk.Button(new_window, text="DONE", bg="red", font=("Regular", 16), command=lambda: add_task_text(task_name.get(), new_window))
    done_button.grid(row= 1, column=0, sticky="nsew")

def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def main_window_exit():
    save_tasks()
    root.destroy()
    

mixer.init()
play_bg_sound()

# ==========================================
#              MAIN GUI SETUP
# ==========================================

root = tk.Tk()
root.iconbitmap("bsu_logo.icon")
root.geometry("750x500")
root.config(bg="red")
root.maxsize(750, 500)
root.protocol("WM_DELETE_WINDOW", main_window_exit)

# for some resposiveness
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# --- LEFT PANEL (Timer) ---

# left frame
left_frame = tk.Frame(root, bg="purple", height=500, width=500)
left_frame.grid_propagate(False)
left_frame.grid(row=0, column=0, sticky="nsew")
left_frame.rowconfigure(0, weight=1)
left_frame.rowconfigure(1, weight=2)
left_frame.rowconfigure(2, weight=1)
left_frame.rowconfigure(3, weight=1)
left_frame.columnconfigure(0, weight=1)

# top frame
top_frame = tk.Frame(left_frame, bg="red", height=100, width=500)
top_frame.grid_propagate(False)
top_frame.grid(row=0, sticky="nsew")
top_frame.rowconfigure(0, weight=1)
top_frame.columnconfigure(0, weight=1)

# hero frame
hero_frame = tk.Frame(left_frame, bg="orange", height=200, width=500)
hero_frame.grid_propagate(False)
hero_frame.grid(row=1, sticky="nsew")
hero_frame.rowconfigure(0, weight=2)
hero_frame.rowconfigure(1, weight=1)
hero_frame.columnconfigure(0, weight=1)

# button frame
button_frame = tk.Frame(left_frame, bg="red", height=100, width=500)
button_frame.grid_propagate(False)
button_frame.grid(row=3, sticky="nsew")
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)
button_frame.rowconfigure(0, weight=1)

# bottom frame
bottom_frame = tk.Frame(left_frame, bg="red", height=100, width=500)
bottom_frame.grid_propagate(False)
bottom_frame.grid(row=4, sticky="nsew")

# timer
pomodoro_counter = tk.Label(top_frame, bg="white", text=values["pomodoro_count"], font=("Regular", 64))
pomodoro_counter.grid(row=0, column=0, sticky="nsew")

timer_label = tk.Label(hero_frame, bg="orange", text="25:00", font=("Regular", 64))
timer_label.grid(row=0,  sticky="nsew")

timer_button = tk.Button(hero_frame, bg="white", text="START", font=("Regular", 26), command=start_timer_controller)
timer_button.grid(row=1)

# buttons
pomodoro_button = tk.Button(button_frame, bg="white", text="Pomodoro", font=("Regular", 20), command=lambda: set_timer(5, "pomodoro"))
pomodoro_button.grid(row=0, column=0, sticky="nsew")

short_button = tk.Button(button_frame, bg="white", text="Short-break", font=("Regular", 20), command=lambda: set_timer(300, "short-timer"))
short_button.grid(row=0, column=1, sticky="nsew")

long_button = tk.Button(button_frame, bg="white", text="Long-break", font=("Regular", 20), command=lambda: set_timer(900, "long-timer"))
long_button.grid(row=0, column=2, sticky="nsew")

""" Right Side of the Program """

# right frames
right_frame = tk.Frame(root, bg="blue", height= 500, width=250)
right_frame.propagate(False)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.columnconfigure(0, weight=1)
right_frame.columnconfigure(1, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_rowconfigure(2, weight=1)

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

retreive_tasks()

root.mainloop()