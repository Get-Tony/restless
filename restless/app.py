"""Restless application."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"


from pathlib import Path

from restless.project import Project

# Working on liquid projects and roles.

db_path_obj = Path("/home/tony/code/production/restless/tmp_site/restless.db")

project = Project(db_path_obj)
project.init()
# TODO: Add a check to see if the project is already initialized.
project.add_role("test", "http://github.com/get-tony/restless")
project.update_roles()
for x in project.list_roles():
    print(f"{x}")
print(project.roles_status())
project.load()
project.remove_role("test")
project.load()
