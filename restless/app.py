"""Restless application."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"


from pathlib import Path

# from restless.ansible_manager import run_project
from restless.project import Project

# Working on liquid projects and roles.

# Temporary project directory.
# tmp_site/
# ├── ansible.cfg # Ansible configuration file.
# ├── inventory
# │   └── hosts # Inventory file.
# ├── project
# │   ├── main.yml # Playbook file.
# │   └── roles
# └── restless.db # Database file.

db_path_obj = Path("/home/tony/code/production/restless/tmp_site/restless.db")

project = Project(db_path_obj)
project.init()
project.load()
roles = [
    {"name": "infra", "repo_url": "http://github.com/get-tony/infra"},
    {
        "name": "connectable",
        "repo_url": "http://github.com/get-tony/connectable",
    },
]
project.add_roles(roles)
# project.remove_roles(["connectable", "infra", "not_a_role""])

# print(project.list_roles())

result = project.run()
# print("-" * 100)
# print(dir(result))
print("-" * 100)
print(result.status)
