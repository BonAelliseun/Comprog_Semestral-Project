import time
import tkinter as tk

# IMPLEMENT THIS CODE TO HAVE GUI SOMEHOW (Made with interactive terminal in-mind only.) yes

# POWER DOWN
def power_down():
  print("\nShutting Down.")
  time.sleep(1)
  print("Shutting Down..")
  time.sleep(1)
  print("Shutting Down...")
  time.sleep(2.5)
  quit()


# POMODORO TIMER APP
def timer_app():
    timer = True
    while timer:
        print("\n=== Pomodoro Timer (WIP) ===")
        time.sleep(0.5)

        while True:
            try:
                time_left = int(input("\nEnter number of seconds: "))

                if time_left > 0:
                    print()
                    break

                if time_left == 0:
                    print("\nYou cannot put 0 seconds.")
                    print("Please enter a positive integer.")
                    time.sleep(0.5)
                
                if time_left < 0:
                    print("\nYou cannot put a negative time.")
                    print("Please enter a positive integer.")
                    time.sleep(0.5)

            except ValueError:
                print("\nPlease enter a positive integer.")
                time.sleep(0.5)
        
        # MAKE CODE SO THAT THE USER DECIDES WHEN TO START THE TIMER
        start = input(f"Type and enter 'START' to start your timer. ({time_left} second/s): ")

        while True:
            if start == 'START': # Loop?
                while time_left > 0:
                    time_left -= 1
                    print(time_left)
                    time.sleep(1)
                    
                if time_left == 0:
                    print("\nTimes up!")
                    choice = input("Would you like to set another timer? (Y/N): ")
                    
                    if choice == 'Y' or choice == 'y':
                        timer = True
                        print()

                    elif choice == 'N' or choice == 'n':
                        timer = False
            else:
                pass # PREVENT THE CODE FROM CONTINUING UNTIL TIMER HAS STARTED AND ENDED.


# MAIN MENU
def main_menu():
    print("\n--- Home Screen ---")
    print("Available Applications:\n")
    time.sleep(0.5)

    print("1. Timer")
    print("2. Power Off")
    print("3. Exit Program")
    time.sleep(0.75)
    
# Suggestion: Make it able to accept words as well? (Such as "timer")

    while True:
        try:   
            app = int(input("\nChoose an application to run. (1-3): "))
            if app == 1:
                timer_app()
                break

            elif app == 2:
                power_down()
                break

            else:
                print("Invalid number. Try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    

# START-UP MESSAGE
print("Desktop Python Software (Alpha 1.0.0)")
print("Loading...")
time.sleep(2)

print("\nWelcome to Dekstop Python Software! A Multi-purpose Personal Productivity App that lets you:")
time.sleep(2)
print("  - Make a To-do list")
time.sleep(1)
print("  - Set-up a timer")
time.sleep(2)
print("  - Uhhhh that's it for now.")
time.sleep(1)

main_menu()

