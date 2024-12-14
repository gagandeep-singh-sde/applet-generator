import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import utilities.toolbox_reader as toolbox_reader
import utilities.applet_generator as applet_generator


class ToolboxFileHandler:
    """
    Handle the uploaded toolbox file.
    """

    def __init__(self, file):
        self.file = file
        self.fs = FileSystemStorage()
        self.file_path = self.fs.save(self.file.name, self.file)
        self.file_path = self.fs.path(self.file_path)

    def process_file(self):
        entries = toolbox_reader.ReadToolboxDB(self.file_path)
        applet = applet_generator.GenerateApplet(entries)
        applet_file_path = os.path.join(os.path.dirname(self.file_path), applet)
        print(applet)
        print(applet_file_path)
        return applet_file_path


def upload_toolbox(request):
    """
    Handle the file upload and return the generated HTML file as a response.
    """
    if request.method == "POST":
        toolbox_file = request.FILES["toolbox_file"]
        handler = ToolboxFileHandler(toolbox_file)
        applet_file_path = handler.process_file()

        if applet_file_path and os.path.exists(applet_file_path):
            with open(applet_file_path, "r", encoding="utf-8") as applet:
                response = HttpResponse(
                    applet.read(),
                    content_type="text/html",
                )
                response["Content-Disposition"] = f'attachment; filename="applet.html"'
                return response

    return render(request, "naskapi/upload.html")
