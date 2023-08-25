from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.CharField(label='Your age')
    bio = forms.CharField(label='Biography', widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError("File should not contain virus")


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
