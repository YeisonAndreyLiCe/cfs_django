import os
from datetime import datetime

class Requirement:
    def __init__(self, description, user_id):
        self.name = f"requirementProject{datetime.now()}{user_id}"
        self.description = description

    def save(self, fileClass):
        path = os.path.join("projects", fileClass, self.name)
        with open(f"{path}.txt", "w") as destination:
            destination.write(self.description)

    def validator(self):
        if self.description == "":
            return False
        return True

class ToDo:
    def __init__(self, description, user_id):
        self.name = f"requirementProject{datetime.now()}{user_id}"
        self.description = description

    def save(self, fileClass):
        path = os.path.join("projects", fileClass, self.name)
        with open(f"{path}.txt", "w") as destination:
            destination.write(self.description)

    def validator(self):
        if self.description == "":
            return False
        return True

class OpenF:
    list = []
    
    def Open(cls, fileClass, filename):
        path = os.path.join("projects",fileClass, filename)
        #path = os.path.join('projects', 'requirements', str(filename))
        with open(f'{path}.txt', "r") as destination:
            cls.list.append(destination.read())
        return cls.list
    