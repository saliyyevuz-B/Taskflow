
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register_view, name="register"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="tasks/login.html"
        ),
        name="login"
    ),

    path("logout/", views.logout_view, name="logout"),

    path(
        "delete/<int:task_id>/",
        views.delete_task,
        name="delete_task"
    ),

    path(
        "edit/<int:task_id>/",
        views.edit_task,
        name="edit_task"
    ),

    path(
        "complete/<int:task_id>/",
        views.complete_task,
        name="complete_task"
    ),
]
