import time
import os
import tkinter as tk


root = tk.Tk()
root.geometry("500x500")


# --- Constants for Timer Durations (in seconds) ---
# 25 minutes * 60 seconds/minute = 1500
POMODORO_TIME = 1500 
# 5 minutes * 60 seconds/minute = 300
SHORT_BREAK_TIME = 300
# 15 minutes * 60 seconds/minute = 900
LONG_BREAK_TIME = 900

# --- Utility Functions ---

def clear_screen():
    # Helper function to clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def format_time_display(seconds):
    """
    Converts total seconds into 'mm:ss' string format for the active countdown display.
    """
    # Calculate minutes and remaining seconds
    mins, secs = divmod(seconds, 60)
    
    # Ensures two digits for minutes and seconds
    return f"{mins:02}:{secs:02}"

def format_time_menu(seconds):
    """
    Converts total seconds into a string showing only minutes for the selection menu.
    """
    # Calculate total minutes by integer division
    mins = seconds // 60
    
    # Ensures two digits for minutes
    return f"{mins:02} minutes"

# --- Timer Selection Function ---

def get_timer_choice():
    """Prompts the user to select a set timer."""
    # The third element is the string used for the menu display (e.g., "25 minutes")
    timer_mapping = {
        '1': ("Pomodoro (Work)", POMODORO_TIME, format_time_menu(POMODORO_TIME)),
        '2': ("Short Break", SHORT_BREAK_TIME, format_time_menu(SHORT_BREAK_TIME)),
        '3': ("Long Break", LONG_BREAK_TIME, format_time_menu(LONG_BREAK_TIME))
    }

    while True:
        clear_screen()
        print("=== 🍅 Pomodoro Timer Selection ===")
        print("\nPlease choose a timer option:")
        # Display the formatted menu string (e.g., "25 minutes")
        print(f"  1. Pomodoro (Work) - {timer_mapping['1'][2]}")
        print(f"  2. Short Break     - {timer_mapping['2'][2]}")
        print(f"  3. Long Break      - {timer_mapping['3'][2]}")
        print("-----------------------------------")
        
        choice = input("Enter option number (1, 2, or 3): ").strip()
        
        if choice in timer_mapping:
            # Returns the timer name and the total seconds
            return timer_mapping[choice][0], timer_mapping[choice][1]
        else:
            print("\n**Invalid choice.** Please enter 1, 2, or 3.")
            time.sleep(1)

# --- Timer Execution Function ---

def start_timer(timer_name, total_seconds):
    """Runs the countdown timer."""
    time_left = total_seconds
    
    # Use the detailed 'mm:ss' format for the confirmation screen
    initial_time_str = format_time_display(total_seconds)
    
    # Wait for the user to type 'START' (Clean screen loop)
    while True:
        clear_screen()
        
        print(f"=== 🍅 {timer_name} Timer ===")
        print(f"\nTime is set for: **{initial_time_str}**") # Displayed in mm:ss
        print("------------------------------")
        print("Type and enter **'START'** to begin the countdown.")
        
        start = input("> ").strip().upper()
        
        if start == 'START':
            break

    # Countdown loop
    while time_left > 0:
        clear_screen()

        # Use the detailed 'mm:ss' format for the active countdown
        display_time = format_time_display(time_left)
        
        print(f"⌛ {timer_name} Remaining: **{display_time}**")

        time.sleep(1)
        time_left -= 1

    # Final clear and "Time's up!" message
    clear_screen()
    print("\n\n######################")
    print(f"## ⏰ {timer_name} Time's up! ##")
    print("######################")


# --- Main Program Loop ---
timer_active = True
while timer_active:
    
    # 1. Get the time selection from the user
    timer_name, total_seconds = get_timer_choice()

    # 2. Start the timer and countdown
    start_timer(timer_name, total_seconds)

    # 3. Ask if the user wants to set another timer
    while True:
        choice = input("Would you like to set another timer? (Y/N): ").upper()

        if choice == 'Y':
            break
        elif choice == 'N':
            timer_active = False
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 'Y' or 'N'.")

time.sleep(1)
clear_screen()