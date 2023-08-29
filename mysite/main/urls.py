from django.urls import path
from .views import main, form

app_name = "main"

urlpatterns = [
    path("", main, name='main_index'),
    path("form/", form, name='main_form'),
]