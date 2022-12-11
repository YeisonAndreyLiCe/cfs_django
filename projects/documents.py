import os
from datetime import datetime
from traceback import print_stack, print_tb

def replace_special_chars(string):
    return string.replace(" ", "").replace(":", "_").replace(".", "-")

# this class is used to represent a document in the project it could be a file or a TODO item or a list of requirements

class File:
    def __init__(self):
        self.name = ""
        self.content = ""
        self.lines = []
        self.id_lines = {}
    
    def save(self, content ,fileClass, user_id):
        content = content + "\n"
        self.name = f"{replace_special_chars(str(datetime.now()))}{user_id}" # we use the date and the user id to create a unique name for the file
        path = os.path.join("projects", fileClass, self.name)
        with open(f"{path}.txt", "w") as destination:
            self.content = content
            destination.write(content)
        return self

    def validator(self, content):
        if content == "":
            return False
        return True
    
    def openFile(self,fileClass, name):
        try:
            path = os.path.join("projects",fileClass, name)
            with open(f'{path}.txt', "r") as destination:
                self.lines = (destination.readlines())
                for i in range(len(self.lines)):
                    if self.lines[i].strip() != "":
                        self.id_lines[i] = self.lines[i]# creating a dictionary with an id for each line to be used in the html
                        self.content += self.lines[i].lstrip() if i == 0 else self.lines[i]               
            return self.id_lines
        except:
            return {'error': f'There is no {fileClass} in this project'}

    def update(self, content ,fileClass, name, user_id):
        if name != "" and name != None:
            path = os.path.join("projects", fileClass, name)
            with open(f"{path}.txt", "w") as destination:
                self.content = content
                destination.write(content)
                self.openFile(fileClass, name)
            return name
        else:
            self.save(content, fileClass, user_id)
            return self.name

    def addLines(self, content, fileClass, name, user_id):
        if name != "" and name != None: 
            path = os.path.join("projects", fileClass, name)
            with open(f"{path}.txt", "r") as destination:
                self.lines = (destination.readlines())
            with open(f"{path}.txt", "a") as destination:
                destination.write("\n" + content)
                #self.openFile(fileClass, name)
            return name
        else:
            self.save(content, fileClass, user_id)
            return self.name

    def deleteLine(self, line_id, fileClass, name):
        path = os.path.join("projects", fileClass, name)
        with open(f"{path}.txt", "w") as destination:
            self.lines.pop(line_id)
            list = []
            for line in self.lines:
                list.append(line) if line !="\n" else None
            self.content = "".join(list)
            destination.write(self.content)
        return self.openFile(fileClass, name)

    def deleteFile(self, fileClass, name):
        try:
            path = os.path.join("projects", fileClass, name)
            os.remove(f"{path}.txt")
            return True
        except:
            return False

class Artefact:
    def __init__(self, id ,description):
        self.id = id
        self.description = description.split("--version")[0]
        self.completed = False

        try:
            self.version = description.split("--version")[1]
        except:
            self.version = "last version"

    def complete(self):
        if '- Completed' in self.description:
            self.completed = True
            #self.description = self.description.replace("- Completed", "")
        return self.completed