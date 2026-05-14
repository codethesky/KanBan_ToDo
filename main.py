from todo import ToDoList
from project import Project
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt

STATUS = ["New", "Pending", "On Hold", "Complete"]
DETAIL = ["title", "status", "description", "preconditions", "reproduction_steps", "actual", "expected", "priority"]

console = Console()


def display_projects(proj):
    proj_list = proj.get_all_projects()
    if not proj_list:
        console.print("\n[yellow]There are no projects found to display![/yellow]\n")
        return
    for num, item in enumerate(proj_list, 1):
        console.print(f"[bold]{num}.[/bold]  {item}")
    console.print()


def get_confirmation(proj, number):
    proj_list = proj.get_all_projects()
    if 0 < number + 1 <= len(proj_list):
        return Confirm.ask(f"Confirm you have selected [bold]{proj_list[number]}[/bold]")
    else:
        console.print("\n[red]Project selection not found.[/red]")
        return False


def get_project_selection(proj, pos):
    proj_list = proj.get_all_projects()
    return proj_list[pos]


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
        console.clear()
        menu_content = (
            "[bold]1.[/bold]  Add Task\n"
            "[bold]2.[/bold]  Open Task\n"
            "[bold]3.[/bold]  Delete Task\n"
            "[bold]4.[/bold]  Change Task Status\n"
            "[bold]5.[/bold]  Display Tasks\n"
            "[bold]6.[/bold]  Exit Project"
        )
        console.print(Panel(menu_content, title="Task Manager", subtitle=f"Project: {proj.project}", border_style="bright_blue", padding=(1, 1)))

        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6"])
        if choice == '1':
            title = Prompt.ask("Enter task title", default="")
            if title:
                status_input = Prompt.ask(f"Enter task status ([1]{STATUS[0]}/[2]{STATUS[1]}/[3]{STATUS[2]}/[4]{STATUS[3]} or press Enter to cancel)", default="")
                status_selection = get_status_selection(status_input)
                if status_selection:
                    todo_list.add_task({'title': title, 'status': status_selection, 'description': '', 'preconditions': '', 'reproduction_steps': '', 'actual': '', 'expected': '', 'priority': ''})
                    todo_list.display_tasks()
                    console.print("[green]Task added successfully.[/green]")
        elif choice == '2':
            todo_list.display_tasks()
            task_index = IntPrompt.ask("Enter task index to open for editing (or 0 to cancel)", default=0)
            if task_index > 0:
                task_index -= 1
                editing_task = True
                while editing_task:
                    console.clear()
                    todo_list.display_task_details(task_index)
                    console.print()
                    edit_menu = (
                        "[bold]1.[/bold]  Title\n"
                        "[bold]2.[/bold]  Status\n"
                        "[bold]3.[/bold]  Description\n"
                        "[bold]4.[/bold]  Preconditions\n"
                        "[bold]5.[/bold]  Reproduction Steps\n"
                        "[bold]6.[/bold]  Actual\n"
                        "[bold]7.[/bold]  Expected\n"
                        "[bold]8.[/bold]  Priority\n"
                        "[bold]0.[/bold]  Exit Task Editor"
                    )
                    console.print(Panel(edit_menu, title="Task Editor", subtitle=f"Project: {proj.project}", border_style="bright_blue", padding=(1, 1)))
                    task_choice = Prompt.ask("Enter the task detail to edit", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"])
                    if task_choice == "0":
                        editing_task = False
                        Prompt.ask("Press Enter to exit the task editor", default="")
                    else:
                        task_choice = int(task_choice) - 1
                        new_detail = Prompt.ask(f"Enter a new [bold]{DETAIL[task_choice]}[/bold] (or press Enter to cancel)", default="")
                        if new_detail:
                            todo_list.change_detail(DETAIL[task_choice], task_index, new_detail)
                            console.clear()
                            todo_list.display_task_details(task_index)
                            console.print("[green]SUCCESS:[/green] Task detail updated.")
                            Prompt.ask("Press Enter to continue", default="")
                        else:
                            Prompt.ask("[yellow]CANCELLED[/yellow]: Press Enter to continue", default="")
        elif choice == '3':
            todo_list.display_tasks()
            task_index = IntPrompt.ask("Enter task index to delete (or 0 to cancel)", default=0)
            if task_index > 0:
                task_index -= 1
                todo_list.delete_task(task_index)
                todo_list.display_tasks()
                console.print("[green]Task deleted successfully.[/green]")
                Prompt.ask("Press Enter to continue", default="")
            else:
                Prompt.ask("[yellow]CANCELLED[/yellow]: Press Enter to continue", default="")
        elif choice == '4':
            todo_list.display_tasks()
            task_index = IntPrompt.ask("Enter task index to change status (or 0 to cancel)", default=0)
            if task_index > 0:
                task_index -= 1
                new_status_prompt = f"Enter new status ([1]{STATUS[0]}/[2]{STATUS[1]}/[3]{STATUS[2]}/[4]{STATUS[3]} or press Enter to cancel)"
                new_status = Prompt.ask(new_status_prompt, default="")
                new_status = get_status_selection(new_status)
                if new_status:
                    todo_list.change_status(task_index, new_status)
                    todo_list.display_tasks()
                    console.print("[green]Task status changed successfully.[/green]")
                    Prompt.ask("Press Enter to continue", default="")
                else:
                    Prompt.ask("[yellow]CANCELLED[/yellow]: Press Enter to continue", default="")
        elif choice == '5':
            todo_list.display_tasks()
            Prompt.ask("Press Enter to continue", default="")
        elif choice == '6':
            proj.clear_project()
            console.print("Exiting project...")
            break


def main():
    running = True
    proj = Project()

    while running:
        console.clear()
        menu_content = (
            "[bold]1.[/bold]  Open a project\n"
            "[bold]2.[/bold]  Create a project\n"
            "[bold]3.[/bold]  Delete a project\n"
            "[bold]4.[/bold]  Exit Application"
        )
        console.print(Panel(menu_content, title="Project Manager", border_style="bright_blue", padding=(1, 1)))

        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"])

        if choice == '1':
            console.clear()
            console.print(Panel("[bold]Project List[/bold]", title="Open a Project", border_style="bright_blue", padding=(1, 1)))
            display_projects(proj)
            project_index = IntPrompt.ask("Enter project to open (or 0 for none)", default=0)
            if project_index > 0:
                project_index -= 1
                if get_confirmation(proj, project_index):
                    selection = get_project_selection(proj, project_index)
                    proj.open_project(selection)
        if choice == '2':
            console.clear()
            console.print(Panel("[bold]Create A Project[/bold]", title="Create A Project", border_style="bright_blue", padding=(1, 1)))
            display_projects(proj)
            project_name = Prompt.ask("Enter a name for the new project (or press Enter to cancel)", default="")
            if project_name and not proj.project_exists(project_name):
                if not proj.create_project(project_name):
                    console.print(f"[red]Failed to create project [bold]{project_name}[/bold]![/red]")
                    console.print("[red]System Failure: Please try again...[/red]")
                    Prompt.ask("Press Enter to continue", default="")
        if choice == '3':
            console.clear()
            console.print(Panel("[bold]Delete A Project[/bold]", title="Delete A Project", border_style="bright_blue", padding=(1, 1)))
            display_projects(proj)
            project_index = IntPrompt.ask("Enter project to delete (or 0 to cancel)", default=0)
            if project_index > 0:
                project_index -= 1
                if get_confirmation(proj, project_index):
                    selection = get_project_selection(proj, project_index)
                    successful = proj.delete_project(selection)
                    if not successful:
                        console.print(f"[red]Failed to delete project [bold]{selection}[/bold]![/red]")
                        Prompt.ask("Press Enter to continue", default="")
        if choice == '4':
            running = False
            console.clear()

        if proj.project_is_open():
            task_menu(proj)


if __name__ == "__main__":
    main()
