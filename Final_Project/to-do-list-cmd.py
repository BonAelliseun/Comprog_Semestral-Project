# DISPLAY LIST FUNCTION
def display_tasks(todo_list):
    print("\n--- CURRENT TASKS ---")
    if not todo_list:
        print("Rats! It's empty.")
    else:
        for index, task in enumerate(todo_list):
            print(f"{index + 1}. {task}")
    print("-" * 21)

# ANNOYING ADD TASK PROMPT
def add_task_prompt(todo_list):
    prompt = input("Would you like to add a task? (Y/N): ").strip().lower()

    if prompt == 'y':
        task = input("\nEnter the task you want to add: ")
        todo_list.append(task)
        print(f"'{task}' has been added.")
        display_tasks(todo_list)
    else:
        pass

# MAIN PROGRAM LOOP
def main():
    todo_list = []

    while True:
        print("\n--- TO-DO LIST MENU ---")
        print("1. Add")
        print("2. View")
        print("3. Edit")
        print("4. Remove")
        print("5. Exit")
        
        choice = input("\nEnter choice (number or word): ").strip().lower()

        # ADD
        if choice == '1' or choice == 'add':
            task = input("\nEnter the task you want to add: ")
            todo_list.append(task)
            print(f"'{task}' has been added.")
            display_tasks(todo_list)

        # VIEW
        elif choice == '2' or choice == 'view':
            display_tasks(todo_list)

        # EDIT
        elif choice == '3' or choice == 'edit':
            if not todo_list:
                print("\nList is empty, nothing to edit.")
                add_task_prompt(todo_list)

            else:
                print("\nSelect a task number to edit:")
                for index, task in enumerate(todo_list):
                    print(f"{index + 1}. {task}")

                task_num = int(input("Enter the task number you want to edit: "))
                task_index = task_num - 1

                if 0 <= task_index < len(todo_list):
                    new_task = input("Enter the new task description: ")
                    old_task = todo_list[task_index]
                    todo_list[task_index] = new_task
                    print(f"Changed '{old_task}' to '{new_task}'.")
                else:
                    print("Invalid task number. Please enter a valid number.")

            display_tasks(todo_list)

        # REMOVE
        elif choice == '4' or choice == 'remove':
            if not todo_list:
                print("\nList is empty, nothing to remove.")
                add_task_prompt(todo_list)
            
            else:
                task_num = input("\nEnter the task number you want to remove: ")
                task_index = task_num - 1

                if 0 <= task_index < len(todo_list):
                    removed_task = todo_list.pop(task_index) 
                    print(f"'{removed_task}' has been removed.")
                    display_tasks(todo_list)
                else:
                    print("Task not found. Could not remove task.")
                    print("Tip: Check for any typographical errors in your input!")
                
                display_tasks(todo_list)

        # EXIT
        elif choice == '5' or choice == 'exit':
            print("Thank you for using the To-Do List Program!")
            break

        else:
            print("ERROR: Invalid input. Please enter a number from (1-5) or the choice.")
            print("Tip: Check for any typographical errors in your input!")

# START
print("To-Do List Program")
print("Version Alpha (3)")

main()