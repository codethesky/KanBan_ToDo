from todo import ToDoList
import os
from project import Project

STATUS = ["New", "Pending", "On Hold", "Complete"]

def display_projects(proj):
    proj_list = proj.get_all_projects()
    if not proj_list:
        print('\nThere are no projects found to display!\n\n')
        return
    for num, item in enumerate(proj_list):
        number = num + 1
        print(f'{number}. {item}')
    print('\n')

# Will check an index in project list and confirm if user selected it
def get_confirmation(proj, number):
    proj_list = proj.get_all_projects()
    if 0 < number + 1 <= len(proj_list):
        choice = input(f'Confirm you have selected {proj_list[number]} (y or n): ')
        if choice.upper() == 'Y': return True
        else: return False
    else:
        print('\nProject selection not found.')
        return False

def get_project_selection(proj, pos):
    proj_list = proj.get_all_projects()
    return proj_list[pos]

def set_title(menu, project=None):
    print(f"\n\t{menu}\n")
    if project is None:
        print('')
    else:
        print(f"\tProject: {project}\n\n")

def get_status_selection(option):
    if option in ['1', '2', '3', '4']:
        option = STATUS[int(option) - 1]
    if option not in STATUS:
        option = ''
    return option

def task_menu(proj):
    working_project = proj.project
    proj_location = proj.get_project_location(working_project)
    task_location = proj.join_file_path(proj_location, 'tasks.json')
    todo_list = ToDoList(task_location)

    while True:
        os.system('cls')
        set_title("Task Manager", proj.project)
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Change Task Status")
        print("4. Display Tasks")
        print("5. Exit Project")

        choice = input("\n\nEnter your choice: \n")

        if choice == '1':
            title = input("Enter task title or select enter to cancel: ")
            status_selection = input(f"Enter task status ((1){STATUS[0]}/(2){STATUS[1]}/(3){STATUS[2]}/(4){STATUS[3]}) or select enter to cancel: ")
            status_selection = get_status_selection(status_selection)
            if title != '' and status_selection != '':
                todo_list.add_task({'title': title, 'status': status_selection})
                todo_list.display_tasks()
                print("Task added successfully.")
        elif choice == '2':
            todo_list.display_tasks()
            task_index = int(input("Enter task index to delete or '0' to cancel: ")) - 1
            if task_index >= 0:
                todo_list.delete_task(task_index)
                todo_list.display_tasks()
                cont = input("\n\nSUCCESS: Select enter to continue. . .")
            else:
                cont = input("\n\nCANCELLED: Select enter to continue. . .")
        elif choice == '3':
            todo_list.display_tasks()
            task_index = int(input("Enter task index to change status or '0' to cancel: ")) - 1
            new_status = input(f"Enter new status ((1){STATUS[0]}/(2){STATUS[1]}/(3){STATUS[2]}/(4){STATUS[3]}) or select enter to cancel: ")
            new_status = get_status_selection(new_status)
            if task_index != '' and task_index >= 0 and new_status != '':
                todo_list.change_status(task_index, new_status)
                todo_list.display_tasks()
                cont = input("\n\nSUCCESS: Select enter to continue. . .")
            else:
                cont = input("\n\nCANCELLED: Select enter to continue. . .")
        elif choice == '4':
            todo_list.display_tasks()
            cont = input("\n\nSelect enter to continue. . . ")
        elif choice == '5':
            proj.clear_project()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    running = True
    proj = Project()

    while running:
        os.system('cls')
        set_title("Project Manager")
        print("1. Open a project")
        print("2. Create a project")
        print("3. Delete a project")
        print("4. Exit Application")
        choice = input("\n\nEnter your choice: ")

        if choice == '1':
            os.system('cls')
            set_title("Project List")
            display_projects(proj)
            project_index = int(input("Enter project to open or 0 for none: ")) - 1
            confirmation = get_confirmation(proj, project_index)
            if confirmation:
                selection = get_project_selection(proj, project_index)
                proj.open_project(selection)
        if choice == '2':
            os.system('cls')
            set_title("Create A Project")
            display_projects(proj)
            project_name = input("Enter a name for the new project or Enter to cancel: ")
            if project_name != '' and not proj.project_exists(project_name):
                if not proj.create_project(project_name):
                    print(f'Failed to create project {project_name}!')
                    print('System Failure: Please try again. . .')
        if choice == '3':
            os.system('cls')
            set_title("Delete A Project")
            display_projects(proj)
            project_index = int(input("Enter project to delete or '0' to cancel: ")) - 1
            confirmation = get_confirmation(proj, project_index)
            if confirmation:
                selection = get_project_selection(proj, project_index)
                successful = proj.delete_project(selection)
                if not successful:
                    print(f'Failed to delete project {selection}!')
        if choice == '4':
            running = False
            os.system('cls')
           
        if proj.project_is_open():
            task_menu(proj)

if __name__ == "__main__":
    main()
