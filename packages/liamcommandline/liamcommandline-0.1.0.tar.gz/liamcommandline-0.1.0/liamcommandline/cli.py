import sys


def options():
    """Returns a list of commands for making a task board."""
    return """Usage: tb <command> [task] [options]
    
    #Commands 
        mark-down <task> - marks down a new task to your task board.
            options: 
                --prio=low/medium/high

        taskboard <file> - shows your taskboard with a nice text. (<file> is taskboard.txt by default)
            

        remove <task> - Remove a task from the taskboard.
            options: 
                    --prio=low/medium/high

        complete <task> - Set a task as complete. 
    """

def process_command(args):
    """Read the arguments for the Taskboard.
    
    Returns a tuple:
        command - should be a string, 'mark-down', 'taskboard', 'remove', 'complete'
        task: should be a string, describes the task if needed.
        prio: should be a string, priority level.
        """
    if not args or '-h' in args or '--help' in args:
        print(options())
        sys.exit(0)

    command = args[0]
    if command not in ['mark-down', 'taskboard', 'remove', 'complete']:
        print("Error: Command must be 'mark-down', 'taskboard, 'remove', 'complete'")
        sys.exit(1)
    
    # Set task and task-prio to none initially to 
    task = None
    prio = None
    if command in ['mark-down', 'taskboard', 'remove', 'complete']:
        if len(args) < 2:
            print(f"Error: Invalid: '{command}' requires <task> field")
            sys.exit(1)
        task_args = [arg for arg in args[1:] if not arg.startswith("--prio=")]
        task = ' '.join(task_args)
        
        
        for arg in args:
            if arg.startswith("--prio="):
                prio = arg.split("=")[1].lower()
                if prio not in ['high', 'medium', 'low']:
                    print("Error: Priority must be 'high', 'medium', or 'low'")
                    sys.exit(1)

    return (command, task, prio)
def manage_taskboard(command, task, prio):
    """Manage the taskboard by marking down tasks, lising the board, removing tasks,
    setting tasks to in-progress, and setting tasks as complete.
    
        command (str): The change you want to make to the taskbar
        task (str): The task you want to target/create.
        prio (str): The priority of the task (high/medium/low)

    Postconditions: Returns a message describing the result of your command.
     """
    file_name = 'taskboard.txt'

    if command == 'mark-down':
        task_input = f"{prio or 'low'}: {task}\n"
        with open(file_name, 'a') as file:
            file.write(task_input)
        return f"Added task: '{task}' with priority {prio or 'low'}"

    elif command == 'taskboard':
        try:
            with open(file_name, 'r') as file:
                tasks = file.readlines()
            if not tasks:
                return "Your taskboard is empty."
            return "".join([f"{i+1}. {t.strip()}\n" for i, t in enumerate(tasks)])
        except FileNotFoundError:
            return "Your taskboard is empty."
    
    elif command == 'remove':
        try:
            with open(file_name, 'r') as file:
                tasks = file.readlines()
            new_tasks = [t for t in tasks if not t.strip().endswith(task)]
            if len(tasks) == len(new_tasks):
                return f"The task '{task}' not found on the board."
            with open(file_name, 'w') as file:
                file.writelines(new_tasks)
            return f"Removed: {task}"
        except FileNotFoundError:
            return "Your taskboard is empty."

    elif command == 'complete':
        try:
            with open(file_name, 'r') as file:
                tasks = file.readlines()
            for i, line in enumerate(tasks):
                if line.strip().endswith(task):
                    tasks[i] = f"Completed: {line.strip()}\n"
                    with open(file_name, 'w') as file:
                        file.writelines(tasks)
                    return f"Marked task '{task}' off the board."
                return f"Task '{task}' not found on the board."

        except FileNotFoundError:
            return "Your taskboard is empty."

def main():
    """Main function that handles logic for the Taskboard and commands.

    Postconditions: will set command, task, and priority to their respective inputted values 
    result calls the function manage_taskboard to perform the command with the args.
    result is printed to the console.
    
    """
    args = sys.argv[1:]
    command, task, priority = process_command(args)
    result = manage_taskboard(command, task, priority)
    print(result)

if __name__ == '__main__':
    main()
    
    




        
