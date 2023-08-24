from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, 'requestdataapp/user-bio-form.html')


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        file_size = fs.size(filename)
        if file_size > 1048576:
            fs.delete(filename)
            print('file is deleted: ', filename)
            error_upload(request)
        else:
            print('file saved as: ', filename)
    return render(request, 'requestdataapp/file-upload.html')


def error_upload(request: HttpRequest) -> HttpResponse:
    return render(request, 'requestdataapp/error-message.html')


def error_request(request: HttpRequest) -> HttpResponse:
    return render(request, 'requestdataapp/error-request.html')
