import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage


def upload_toolbox(request):
    if request.method == "POST":
        toolbox_file = request.FILES["toolbox_file"]
        fs = FileSystemStorage()
        file_path = fs.save(toolbox_file.name, toolbox_file)
        file_path = fs.path(file_path)

        applet_file_path = process_toolbox_file(file_path)

        with open(applet_file_path, "r", encoding="utf-8") as applet:
            response = HttpResponse(
                applet.read(),
                content_type="text/html",
            )
            response["Content-Disposition"] = f'attachment; filename="applet.html"'
            return response

    return render(request, "naskapi/upload.html")


def process_toolbox_file(file_path):
    applet_file_path = os.path.join(os.path.dirname(file_path), "applet.html")
    with open(applet_file_path, "w", encoding="utf-8") as f:
        f.write("<html><body><h1>Applet Content</h1></body></html>")
    return applet_file_path
