import tkinter as tk
from pygame import mixer
import os
import customtkinter as ctk
from tkinter import font
from PIL import Image
from pathlib import Path

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

highlight_color = "#FA955E"

def play_bg_sound():
    path = os.path.dirname(__file__)
    path = os.path.join(path, "sounds", "bg.ogg")
    mixer.music.load(f"{path}")
    mixer.music.play(-1)

def load_file(folder_name, file_name):
    path = os.path.dirname(__file__)
    path = os.path.join(path, folder_name, str(file_name))
    return path

def change_display_timer():
        display_time = format_time_display(values["timer"])
        timer_label.configure(text=display_time)

def format_time_display(seconds):
    """
    Converts total seconds into 'mm:ss' string format for the active countdown display.
    """
    # Calculate minutes and remaining seconds
    mins, secs = divmod(seconds, 60)
    
    # Ensures two digits for minutes and seconds
    return f"{mins:02}:{secs:02}"

def start_timer_controller():
    if timer_button.cget("text")== "START":
        values["can_run"] = True
        if values["cur_timer"] == None:
            start_timer()
        timer_button.configure(text="PAUSE")

    elif timer_button.cget("text") == "PAUSE":
        timer_button.configure(text="START")
        values["can_turn"] = True
        root.after_cancel(values["cur_timer"])
        values["cur_timer"] = None
        values["timer"] += 1

    clicked_sound()

def start_timer():
    """Runs the countdown timer."""
    if values["timer"] >= 0 and values["can_run"]: # only starts if timer is not 0 and if it can startvalues[2]
        change_display_timer()
        values["cur_timer"] = root.after(1000, start_timer) # stores current timer 
        values["timer"] -= 1
    elif values["timer"] <= 0 and values["can_run"]:
        if values["timer_tpye"] == "pomodoro":
            values["pomodoro_count"] += 1
        timer_button.configure(text="START")
        
        if values["timer_tpye"] == "pomodoro" and values["pomodoro_count"] % 4 == 0:
            set_timer(900, "long-break")
        elif values["timer_tpye"] == "short-break" or values["timer_tpye"] == "long-break":
            set_timer(300, "pomodoro")
        else:
            set_timer(1500, "short-break")
        
        alarm_file = load_file("sounds", "music3.wav")
        alarm = mixer.Sound(alarm_file)
        alarm.play()
 

def set_timer(seconds, type):
    values["timer_tpye"] = type

    values["timer"] = seconds
    values["can_run"] = False
    if values["cur_timer"] != None:
        root.after_cancel(values["cur_timer"])
        values["cur_timer"] = None
    change_display_timer()
    timer_button.configure(text="START")
    clicked_sound()

def update_task(button_content):
    button_content.configure(state="disabled")
    def edit_text(event):
        def edit():
            if len(task_name.get()) > 0:
                button_content.configure(text=task_name.get())
            button_content.configure(state="disabled")
            edit_text_window.destroy()
            button_content.configure(state="normal")
            clicked_sound()

        update_window.destroy()
        edit_text_window = tk.Toplevel(root) 
        edit_text_window.title("Edit task")
        edit_text_window.configure(bg="black")
        edit_text_window.geometry("200x100") 
        edit_text_window.maxsize(200, 50)
        edit_text_window.columnconfigure(0, weight=1)
        edit_text_window.columnconfigure(1, weight=1) 
        edit_text_window.protocol("WM_DELETE_WINDOW", 
                                  lambda: enable_button(button_content, edit_text_window))

        task_name = tk.Entry(edit_text_window, 
                             width=edit_text_window.winfo_reqwidth())
        task_name.grid(row= 0, column=0, sticky="nsew")

        done_button = ctk.CTkButton(edit_text_window, 
                                text="DONE", 
                                fg_color="black",
                                text_color="white",
                                hover_color=highlight_color,
                                font=("Arial Black", 16), 
                                command=edit)
        done_button.grid(row= 1, column=0, sticky="nsew")
        clicked_sound()
        
    def done(event):
        update_window.destroy()
        button_content.destroy()
        values["task_number"] -= 1
        clicked_sound()
        
    update_window = tk.Toplevel(root) 
    update_window.title("update window") 
    update_window.columnconfigure(0, weight=1)
    update_window.columnconfigure(1, weight=1)
    update_window.protocol("WM_DELETE_WINDOW", 
                           lambda: enable_button(button_content, update_window))

    edit_button = ctk.CTkButton(update_window, 
                            text="Edit", 
                            fg_color="black",
                            hover_color=highlight_color,
                            font=("Arial Black", 16))
    done_button = ctk.CTkButton(update_window, 
                            text="done", 
                            fg_color="black",
                            hover_color=highlight_color,
                            font=("Arial Black", 16))

    edit_button.grid(row=0, column=0, sticky="nsew")
    done_button.grid(row=0, column=1, sticky="nsew")

    edit_button.bind("<Button-1>", edit_text)
    done_button.bind("<Button-1>", done)
    clicked_sound()

def enable_button(button, window):
    button.configure(state="normal")
    window.destroy()

def add_task_text(task_name, window=None):
    if len(task_name) > 0:      
        new_task = ctk.CTkButton(master=scrollable_frame, 
                                 text=task_name, 
                                 font=("Arial Black", 12), 
                                 fg_color="#5D5D5D", 
                                 hover_color=highlight_color,
                                 anchor="nw", 
                                 command=lambda: update_task(new_task))
        new_task.propagate(False)
        new_task.grid(row=values["task_number"], column=0, sticky="ew", padx=5, pady=2)  
        values["task_number"] += 1
    
    add_task_button.configure(state="normal")

    if window != None:
        window.destroy()
        clicked_sound()
    

def save_tasks():
    """Save all tasks from scrollable_frame to a file"""
    tasks = scrollable_frame.winfo_children()
    
    if not tasks:
        print("No tasks to save")
        return False
    
    try:
        tasks_file = Path("tasks.txt")
        
        task_texts = []
        for task_widget in tasks:
            try:
                task_text = task_widget.cget("text")
                task_text = task_text.strip()
                if task_text:
                    task_texts.append(task_text)
            except Exception as widget_error:
                print(f"Warning: Could not get text from widget: {widget_error}")
                continue
        
        with open(tasks_file, "w", encoding="utf-8") as f:
            for task_text in task_texts:
                f.write(task_text + "\n") 
        
        print(f"Saved {len(task_texts)} tasks to {tasks_file}")
        return True
        
    except Exception as ex:
        print(f"Error saving tasks: {ex}")
        return False


def retrieve_tasks():
    """Retrieve and display tasks from file"""
    try:
        tasks_file = Path("tasks.txt")
        
        if not tasks_file.exists():
            print("No tasks file found. Starting with empty task list.")
            tasks_file.touch()
            return []
        
        if tasks_file.stat().st_size == 0:
            print("Tasks file is empty")
            return []

        with open(tasks_file, "r", encoding="utf-8") as f:
            tasks = [line.rstrip('\n') for line in f.readlines()] 
        
        tasks = [task for task in tasks if task.strip()]

        task_count = 0
        for task_text in tasks:
            if task_text:  
                add_task_text(task_text)
                task_count += 1
        
        print(f"Loaded {task_count} tasks from {tasks_file}")
        return tasks
        
    except PermissionError:
        print("Permission denied: Cannot read tasks.txt")
        return []
    except Exception as ex:
        print(f"Error loading tasks: {ex}")
        # Create file if it doesn't exist
        try:
            Path("tasks.txt").touch()
            print("Created empty tasks file")
        except:
            pass
        return []


def add_new_task():
    add_task_button.configure(state="disabled")

    new_window = tk.Toplevel(root)  # Create a new window
    new_window.title("add new task")
    new_window.geometry("250x100") 
    new_window.configure(bg="black")
    new_window.maxsize(250, 100)
    new_window.columnconfigure(0, weight=1)
    new_window.rowconfigure(0, weight=1)
    new_window.rowconfigure(1, weight=2)
    new_window.protocol("WM_DELETE_WINDOW", lambda: enable_button(add_task_button, new_window))

    task_name = tk.Entry(new_window)
    task_name.grid(row= 0, column=0, sticky="nsew")

    done_button = ctk.CTkButton(new_window, 
                            text="DONE", 
                            fg_color="black", 
                            font=("Arial Black", 16), 
                            hover_color=highlight_color,
                            border_color=highlight_color,
                            border_width=2,
                            text_color="white",
                            command=lambda: add_task_text(task_name.get(), new_window))
    done_button.grid(row= 1, column=0)
    clicked_sound()

def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def main_window_exit():
    save_tasks()
    root.destroy()
    
def title(parent, bg_color):
    border_frame = tk.Frame(parent, background="red") # Border color
    border_frame.grid(row=0, column=0, sticky="nsew")

    frame = tk.Frame(parent, bg=bg_color)
    frame.grid(row=0, column=0, pady=(0, 5), sticky='nsew')
    title_font = font.Font(family="Arial Black", size=18, weight="normal")

    left_label = tk.Label(frame, text="Tomato", font=title_font, fg="red", bg=bg_color)
    left_label.pack(side="left", anchor="sw")

    left_label = tk.Label(frame, text="-Do List", font=title_font, fg="white", bg=bg_color)
    left_label.pack(side="left", anchor="sw")

def clicked_sound():
    clicked_sound_file = load_file("sounds", "button_clicked.mp3")
    clicked_sound = mixer.Sound(clicked_sound_file)
    clicked_sound.play()

mixer.init()
play_bg_sound()



# ==========================================
#              MAIN GUI SETUP
# ==========================================

root = tk.Tk()
root.iconbitmap("bsu_logo.ico")
root.geometry("750x500")
root.configure(bg="black")
root.maxsize(750, 500)
root.protocol("WM_DELETE_WINDOW", main_window_exit)

# for some resposiveness
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# --- LEFT PANEL (Timer) ---

# left frame
left_frame = tk.Frame(root, height=500, width=500, bg="black")
left_frame.grid_propagate(False)
left_frame.grid(row=0, column=0, sticky="nsew")
left_frame.rowconfigure(0, weight=1)
left_frame.rowconfigure(1, weight=2)
left_frame.rowconfigure(2, weight=1)
left_frame.rowconfigure(3, weight=1)
left_frame.columnconfigure(0, weight=1)

# top frame
top_frame = tk.Frame(left_frame, height=100, width=500, bg="black")
top_frame.grid_propagate(False)
top_frame.grid(row=0, sticky="nsew")
top_frame.rowconfigure(0, weight=1)
top_frame.columnconfigure(0, weight=1)

# hero frame
hero_frame = tk.Frame(left_frame, height=200, width=500,bg="black")
hero_frame.grid_propagate(False)
hero_frame.grid(row=1, sticky="nsew")
hero_frame.rowconfigure(0, weight=2)
hero_frame.rowconfigure(1, weight=1)
hero_frame.columnconfigure(0, weight=1)

# button frame
button_frame = tk.Frame(left_frame, height=100, width=500,bg="black")
button_frame.grid_propagate(False)
button_frame.grid(row=3, sticky="nsew")
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)
button_frame.rowconfigure(0, weight=1)

# bottom frame
bottom_frame = tk.Frame(left_frame, 
                        height=100, 
                        width=500, 
                        bg="black")
bottom_frame.grid_propagate(False)
bottom_frame.grid(row=4, sticky="nsew")

# timer
title(top_frame, "black")


timer_label = tk.Label(hero_frame, 
                       bg="black", 
                       text="25:00", 
                       font=("Arial Black", 80),
                       fg=("white")
                       )
timer_label.grid(row=0,  sticky="nsew")

start_image_path = load_file("images", "start-orange.png")
start_image = ctk.CTkImage(light_image=Image.open(start_image_path),
                           size=(40, 40))

timer_button = ctk.CTkButton(master=hero_frame,
                             image=start_image,
                             corner_radius=20, 
                             text="START",
                             hover_color= highlight_color,
                             command=start_timer_controller,
                             fg_color="transparent",
                             font=("Arial Bold", 16),
                             width=40,
                             height=40)
timer_button.grid(row=1)

# buttons
pomodoro_image_path = load_file("images", "pomodoro.png")
pomodoro_image = ctk.CTkImage(light_image=Image.open(pomodoro_image_path),
                           size=(40, 40))
pomodoro_button = ctk.CTkButton(master=button_frame, 
                                image=pomodoro_image,
                                fg_color="white", 
                                text_color = "black",
                                hover_color= highlight_color,
                                text="Pomodoro", 
                                border_width=0,
                                font=("Arial Bold", 12), 
                                command=lambda: set_timer(1500, "pomodoro"),
                                corner_radius=75,
                                anchor="w"
                                )
pomodoro_button.grid(row=0, column=0, sticky="nsew", pady=20, padx=15)


short_image_path = load_file("images", "short.png")
short_image = ctk.CTkImage(light_image=Image.open(short_image_path),
                           size=(40, 40))
short_button = ctk.CTkButton(master=button_frame, 
                             image=short_image,
                             fg_color="white", 
                             text_color="black",
                             hover_color= highlight_color,
                             text="Short-break", 
                             font=("Arial Bold", 12), 
                             command=lambda: set_timer(300, "short-timer"),
                             corner_radius=75,
                             anchor="w"
                             )
short_button.grid(row=0, column=1, sticky="nsew", pady=20, padx=15)

long_image_path = load_file("images", "long.png")
long_image = ctk.CTkImage(light_image=Image.open(long_image_path),
                           size=(40, 40))
long_button = ctk.CTkButton(master=button_frame, 
                            image=long_image,
                            fg_color="white", 
                            text_color="black",
                            hover_color= highlight_color,
                            text="Long-break", 
                            font=("Arial Bold", 12), 
                            command=lambda: set_timer(900, "long-timer"),
                            corner_radius=75,
                            anchor="w"
                            )
long_button.grid(row=0, column=2, sticky="nsew", pady=20, padx=15, )

""" Right Side of the Program """

# right frames
right_frame = tk.Frame(root, bg="#A48282", height= 500, width=250)
right_frame.propagate(False)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.columnconfigure(0, weight=1)
right_frame.columnconfigure(1, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_rowconfigure(2, weight=1)

to_do_list_title = tk.Label(right_frame,
                            text="Note", 
                            font=("Arial Black", 12), 
                            fg="Black", 
                            bg="#636363", 
                            anchor="sw", 
                            width=5, 
                            height=3 )
to_do_list_title.grid(row=0, column=0, columnspan=2, sticky="nsew")

add_task_button = ctk.CTkButton(right_frame, 
                                text="Add New Task", 
                                font=("Arial Black", 18), 
                                command=add_new_task,
                                hover_color=highlight_color,
                                fg_color="#A48282",
                                corner_radius=0
                                )
add_task_button.grid(row=1, column=0, columnspan=2, sticky="nsew")

canvas = tk.Canvas(right_frame, 
                   bg="#A48282", 
                   width=230, 
                   height=400, 
                   borderwidth=0,
                   highlightthickness=0,
                   relief='flat'
                   )

canvas.grid(row=2, column=0, sticky="nsew")
canvas.rowconfigure(0, weight=1)
canvas.columnconfigure(0, weight=1)

scrollbar = ctk.CTkScrollbar(right_frame, 
                             orientation="vertical", 
                             command=canvas.yview,
                             button_hover_color="#2b2b2b",      # Scrollbar button color
                             button_color="#3b3b3b",
                             )
scrollbar.grid(row=2, column=1, sticky="nsew")

canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas, bg="#A48282", )
scrollable_frame.columnconfigure(0, weight=1)
scrollable_frame.propagate(False)
scrollable_frame.bind("<Configure>", update_scrollregion)

canvas.create_window((0, 0), 
                     window=scrollable_frame, anchor="nw",
                     width=canvas.winfo_reqwidth())
scrollable_frame.grid_columnconfigure(0, weight=1)

retrieve_tasks()

root.mainloop()