from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView,
                                  CreateView,
                                  UpdateView,
                                  ListView,
                                  DetailView)
from django.views import View
from .models import Profile


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class ProfilesListView(ListView):
    template_name = 'myauth/users_list.html'
    model = User
    context_object_name = "users"


class ProfileDetailsView(DetailView):
    template_name = 'myauth/user-details.html'
    model = User
    context_object_name = "user"


class ProfileUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = 'bio', 'avatar'
    template_name_suffix = "_update_form"

    permission_required = "myauth.change_profile"

    def test_func(self):
        if self.request.user.is_staff or self.request.user.id == self.get_object().user.id:
            return True

        has_edit_perm = self.request.user.has_perm("myauth.change_profile")

        return has_edit_perm

    def get_success_url(self):
        return reverse(
            "myauth:user-details",
            kwargs={"pk": self.object.id},
        )

    # def get_object(self, queryset=None):
    #     return self.request.user.profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)

        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        else:
            return render(request, 'myauth/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {"error": "Invalid Login Credentials"})


# @user_passes_test(lambda u: u.is_super)
# def set_cookie_view(request: HttpRequest) -> HttpResponse:
#     response = HttpResponse("Cookie set")
#     response.set_cookie('fizz', 'buzz', max_age=3600)
#     return response
#
#
# def get_cookie_view(request: HttpRequest) -> HttpResponse:
#     value = request.COOKIES.get('fizz', 'default_value')
#     return HttpResponse(f"Cookie value: {value!r}")
#
#
# @permission_required("myauth.view_profile", raise_exception=True)
# def set_session_view(request: HttpRequest) -> HttpResponse:
#     request.session["foobar"] = "spameggs"
#     return HttpResponse('Session Set!')
#
#
# @login_required
# def get_session_view(request: HttpRequest) -> HttpResponse:
#     value = request.session.get("foobar", "default")
#     return HttpResponse(f"Session value: {value!r}")


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

# class FooBarView(View):
#     def get(self, request: HttpRequest) -> JsonResponse:
#         return JsonResponse({"foo": "bar", "spam": "eggs"})
