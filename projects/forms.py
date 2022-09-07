from django import forms
from datetime import datetime
import os


class UploadFileRequirements(forms.Form):
    title = 'requirementProject' + str(datetime.now())
    
    def handle_uploaded_file(cls, f):
        path = os.path.join('projects', 'requirements', cls.title)
        with open(str(path)+'.txt', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def validator(cls):
        if cls.file.size < 0:
            return False
        return True

class UploadFileToDO(forms.Form):
    title = 'requirementProject' + str(datetime.now())
    file = request.FILES['requirements']

    def handle_uploaded_file(cls, f):
        path = os.path.join('ToDo', 'requirements', cls.title)
        with open(str(path)+'.txt', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def validator(cls):
        if cls.file.size < 0:
            return False
        return True