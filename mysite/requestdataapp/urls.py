from django.urls import path
from .views import process_get_view, user_form, handle_file_upload, error_upload, error_request

app_name = "requestdataapp"

urlpatterns = [
    path("get/", process_get_view, name='get_view'),
    path('bio/', user_form, name='user-form'),
    path('upload/', handle_file_upload, name='file-upload'),
    path('error-upload/', error_upload, name='error-upload'),
    path('error-request', error_request, name='error-request')
]