
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Task


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "tasks/register.html", {"form": form})


@login_required
def home(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description
            )

        return redirect("home")

    tasks = Task.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "tasks/home.html", {"tasks": tasks})


@login_required
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(
            Task,
            id=task_id,
            user=request.user
        )
        task.delete()

    return redirect("home")


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            task.title = title
            task.description = description
            task.save()

            return redirect("home")

    return render(request, "tasks/edit.html", {"task": task})


@login_required
def complete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(
            Task,
            id=task_id,
            user=request.user
        )

        task.is_completed = not task.is_completed
        task.save()

    return redirect("home")


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")

    return redirect("home")
