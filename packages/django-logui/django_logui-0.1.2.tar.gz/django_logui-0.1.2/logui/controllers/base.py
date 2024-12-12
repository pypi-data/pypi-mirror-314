import os

from adjango.decorators import controller
from django.http import FileResponse, JsonResponse, Http404
from django.shortcuts import render

from logui.conf import LOGUI_CONTROLLERS_SETTINGS, LOGS_DIR

ctrl_settings = LOGUI_CONTROLLERS_SETTINGS


@controller(**ctrl_settings)
def download_log_file_view(_request, folder_name, file_name):
    if folder_name == '':
        file_path = os.path.join(LOGS_DIR, file_name)
    else:
        file_path = os.path.join(LOGS_DIR, folder_name, file_name)
    if not os.path.exists(file_path):
        raise Http404("Log file not found")
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)


@controller(**ctrl_settings)
def log_folders_view(request):
    try:
        entries = os.listdir(LOGS_DIR)
    except FileNotFoundError:
        raise Http404("Logs directory not found")

    folders = []
    root_files = []
    for f in entries:
        path = os.path.join(LOGS_DIR, f)
        if os.path.isdir(path):
            folders.append(f)
        elif os.path.isfile(path) and '.log' in f:
            # Это лог-файл в корневой директории
            root_files.append(f)

    return render(request, 'logui/log_folders.html', {
        'folders': folders,
        'root_files': root_files
    })


@controller(**ctrl_settings)
def log_files_view(request, folder_name):
    folder_path = os.path.join(LOGS_DIR, folder_name)
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        raise Http404("Folder not found")
    try:
        files = [f for f in os.listdir(str(folder_path)) if os.path.isfile(os.path.join(str(folder_path), f))]
    except FileNotFoundError:
        raise Http404("No log files found in the folder")
    return render(request, 'logui/log_files.html', {'folder_name': folder_name, 'files': files})


@controller(**ctrl_settings)
def log_file_view(request, folder_name, file_name):
    if folder_name == '':
        file_path = os.path.join(LOGS_DIR, file_name)
    else:
        file_path = os.path.join(LOGS_DIR, folder_name, file_name)

    if not os.path.exists(file_path):
        raise Http404("Log file not found")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            log_content = file.read()
    except Exception as e:
        raise Http404(f"Error reading log file: {str(e)}")

    return render(request, 'logui/log_file.html', {
        'folder_name': folder_name,
        'file_name': file_name,
        'log_content': log_content
    })


@controller(**ctrl_settings)
def api_log_file_view(_request, folder_name, file_name):
    if folder_name == '':
        file_path = os.path.join(LOGS_DIR, file_name)
    else:
        file_path = os.path.join(LOGS_DIR, folder_name, file_name)

    if not os.path.exists(file_path):
        return JsonResponse({'error': 'Log file not found'}, status=404)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            log_content = file.read()
        return JsonResponse({'log_content': log_content})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
