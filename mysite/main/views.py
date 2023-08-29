from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def main(request: HttpRequest) -> render:
    return render(request, 'main/index.html')


def form(request: HttpRequest) -> render:
    return render(request, 'main/form.html')
