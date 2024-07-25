import os
import logging
from datetime import datetime

# Globals
PROJ_FOLDER = "Projects/"
LOGGING_LEVEL = "logging.WARNING"
LOGS_LOC = "AppData/system.log"

logging.basicConfig(filename=LOGS_LOC, level=logging.INFO)


class Project:

    def get_current_datetime(self):
        dt = datetime.now()
        return dt.strftime("%m/%d/%y, %H:%M:%S")

    def set_working_project(self, proj_name):
        self.project = proj_name.title()

    def join_file_path(self, part_one, part_two):
        return os.path.join(part_one, part_two)

    def dir_exists(self, dir_name, dir_path=PROJ_FOLDER):
        path = self.join_file_path(dir_path, dir_name)
        return os.path.exists(path)
    
    def project_exists(self, proj_name):
        path = self.join_file_path(PROJ_FOLDER, proj_name)
        return os.path.exists(path)

    def get_project_location(self, proj_name):
        return os.path.join(PROJ_FOLDER, proj_name, "")

    def create_dir(self, dir_name, dir_path=PROJ_FOLDER):
        try:
            path = self.join_file_path(dir_path, dir_name)
            os.mkdir(path)
        except:
            dt = self.get_current_datetime()
            logging.error('{}, Module: Storage, Method: create_dir, Message: Create dir has failed in Storage.create_dir({})'.format(dt, dir_name))

    def get_all_projects(self):
        items = os.listdir(PROJ_FOLDER)
        projects = []
        for item in items:
            path = os.path.join(PROJ_FOLDER, item)
            if os.path.isdir(path):
                projects.append(item)
        return projects

                
    # Recursive function will delete all contents in a directory
    def del_dir(self, dir_name, dir_path=PROJ_FOLDER):
        path = self.join_file_path(dir_path, dir_name)
        all_items = os.listdir(path)
        if not all_items:
            os.rmdir(path)
        else: 
            for item in all_items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    self.del_dir(item, path)
                elif os.path.isfile(item_path):
                    try:
                        os.remove(item_path)
                    except:
                        dt = self.get_current_datetime()
                        logging.error('{}, Module: Storage, Method: del_dir(), Message: Failed to delete file {} in del_dir!'.format(dt, item_path))
            os.rmdir(path)

##############################################################

    # Returns false if the directory is not available, true if it exists
    def delete_project(self, dir_name, dir_path=PROJ_FOLDER):
        directory = dir_name.title()
        if self.dir_exists(directory, dir_path):
            self.del_dir(directory, dir_path)
        return self.dir_exists(directory, dir_path)

    def project_is_open(self):
        if self.project is None: return False
        return True

    def open_project(self, proj_name):
        self.set_working_project(proj_name)

    # Gets all projects that have been created
    def get_project_list(self):
        return self.get_all_projects()

    def is_existing_project(self, proj_name):
        return self.project_exists(proj_name)

    def clear_project(self):
        self.project = None

    # Will create project directory with needed files and directories
    def create_project(self, proj_name):
        name = proj_name.title()
        if self.project_exists(name):
            dt = self.get_current_datetime()                
            logging.warning('{}, Module: {}, Method: create_project(), Message: Project {} already exists!'.format(dt, MODULE, name))
            return False 
        self.create_dir(name)
        project_path = self.join_file_path(PROJ_FOLDER, name)
        if self.project_exists(name):
            path = self.get_project_location(name)
            self.set_working_project(name)
            return True
        return False

    def __init__(self):
        self.project = None

