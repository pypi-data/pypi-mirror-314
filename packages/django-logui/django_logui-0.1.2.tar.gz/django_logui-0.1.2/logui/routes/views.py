from django.urls import path

from logui.controllers.base import (
    log_folders_view, log_files_view, log_file_view,
    download_log_file_view, api_log_file_view
)

app_name = 'logui'

urlpatterns = [
    path('', log_folders_view, name='log_folders'),

    # Маршруты для файлов в корневом каталоге:
    path('file/<str:file_name>/', log_file_view, {'folder_name': ''}, name='log_file_root'),
    path('file/<str:file_name>/download/', download_log_file_view, {'folder_name': ''}, name='log_file_download_root'),
    path('api/file/<str:file_name>/', api_log_file_view, {'folder_name': ''}, name='api_log_file_root'),

    # Маршруты для папок:
    path('dir/<str:folder_name>/', log_files_view, name='log_files'),
    path('dir/<str:folder_name>/<str:file_name>/', log_file_view, name='log_file'),
    path('dir/<str:folder_name>/<str:file_name>/download/', download_log_file_view, name='log_file_download'),
    path('api/<str:folder_name>/<str:file_name>/', api_log_file_view, name='api_log_file'),
]
