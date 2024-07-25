import json
from prettytable import PrettyTable

STATUS = ["New", "Pending", "On Hold", "Complete"]
DISPLAY_COUNT = 0

class ToDoList:
    # filename needs to have complete path as well
    def __init__(self, filename):
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def get_task_index_from_display_selection(self, task_index):
        global DISPLAY_COUNT
        DISPLAY_COUNT = 0
        new = self.get_status_list(STATUS[0])
        pending = self.get_status_list(STATUS[1])
        on_hold = self.get_status_list(STATUS[2])
        complete = self.get_status_list(STATUS[3])
        count = self.get_max_length(new, pending, on_hold, complete)
        task_title = ""
        for num in range(count):
            if num < len(new) and len(new) != 0: 
                DISPLAY_COUNT += 1
                if DISPLAY_COUNT == task_index:
                    task_title = new[num]
            if num < len(pending) and len(pending) != 0: 
                DISPLAY_COUNT += 1
                if DISPLAY_COUNT == task_index:
                    task_title = pending[num]                   
            if num < len(on_hold) and len(on_hold) != 0: 
                DISPLAY_COUNT += 1
                if DISPLAY_COUNT == task_index:
                    task_title = on_hold[num] 
            if num < len(complete) and len(complete) != 0: 
                DISPLAY_COUNT += 1
                if DISPLAY_COUNT == task_index:
                    task_title = complete[num] 
        task_index = None
        for index_count, task in enumerate(self.tasks):
            if task['title'] == task_title:
                task_index = index_count
        return task_index

    def delete_task(self, task_index):
        task_index += 1
        task_index = self.get_task_index_from_display_selection(task_index)
        if task_index is not None:
            del self.tasks[task_index]
        self.save_tasks()
        print('Task has been deleted!')

    def change_status(self, task_index, new_status):
        task_index += 1
        task_index = self.get_task_index_from_display_selection(task_index)
        if task_index is not None:
            self.tasks[task_index]['status'] = new_status
        self.save_tasks()
        print("Task status changed successfully.")

    def get_status_list(self, status) -> list:
        if not self.tasks:
            return []
        status_list = []
        for task in self.tasks:
            if task['status'] == status:
                status_list.append(task['title'])
        return status_list

    def get_max_length(self, *lists):
        if not lists: return 0
        max_length = max(len(status_list) for status_list in lists)
        return max_length

    def get_display_title(self, count, task):
        global DISPLAY_COUNT
        if count >= len(task) or len(task) == 0: return " "
        DISPLAY_COUNT += 1
        return "(" + str(DISPLAY_COUNT) + ") " + task[count]

    def display_tasks(self):
        if self.tasks:
            global DISPLAY_COUNT
            DISPLAY_COUNT = 0
            table = PrettyTable()
            table.field_names = STATUS
            new = self.get_status_list(STATUS[0])
            pending = self.get_status_list(STATUS[1])
            on_hold = self.get_status_list(STATUS[2])
            complete = self.get_status_list(STATUS[3])
            count = self.get_max_length(new, pending, on_hold, complete)

            for num in range(count):
                table.add_row([
                    self.get_display_title(num, new),
                    self.get_display_title(num, pending),
                    self.get_display_title(num, on_hold),
                    self.get_display_title(num, complete)
                    ])
            table.align = 'l'
            print(table)
        else:
            print("No tasks to display.")
