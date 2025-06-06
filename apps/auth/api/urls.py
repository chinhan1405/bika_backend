from django.urls import path

from knox import views as knox_views

from . import views

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        knox_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "logout/all/",
        knox_views.LogoutAllView.as_view(),
        name="logout-all",
    ),
    path(
        "signup/",
        views.SignupView.as_view(),
        name="signup",
    ),
    path(
        "password/reset/",
        views.PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        "password/reset/confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password/change/",
        views.ChangePasswordView.as_view(),
        name="password-change",
    ),
]
