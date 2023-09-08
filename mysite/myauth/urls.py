from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
                    # set_cookie_view,
                    # get_cookie_view,
                    # set_session_view,
                    # get_session_view,
                    MyLogoutView,
                    AboutMeView,
                    RegisterView,
                    ProfileUpdateView,
                    ProfilesListView,
                    ProfileDetailsView,
                    # FooBarView,
)

app_name = "myauth"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True,
        ),
        name='login'),

    # path("cookie/get/", get_cookie_view, name='cookie-get'),
    # path('cookie/set/', set_cookie_view, name='cookie-set'),
    #
    # path("session/set/", set_session_view, name='session-set'),
    # path('session/get/', get_session_view, name='session-get'),

    path('logout/', MyLogoutView.as_view(), name='logout'),

    path('register/', RegisterView.as_view(), name='register'),

    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('details/<int:pk>/', ProfileDetailsView.as_view(), name='user-details'),
    path('list/', ProfilesListView.as_view(), name='users-list'),

    path('update/<int:pk>/', ProfileUpdateView.as_view(), name='update'),

    # path('foo-bar/', FooBarView.as_view(), name="foo-bar"),
]
