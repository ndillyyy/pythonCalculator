from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, TaskForm
from .models import Task

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("task_list")
    else:
        form = RegisterForm()
    return render(request, "tasks/register.html", {"form": form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    filter_by = request.GET.get("filter", "all")
    if filter_by == "pending":
        tasks = tasks.filter(done=False)
    elif filter_by == "done":
        tasks = tasks.filter(done=True)
    return render(request, "tasks/task_list.html", {
        "tasks": tasks, "filter_by": filter_by
    })

@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, "Task created!")
        return redirect("task_list")
    return render(request, "tasks/task_form.html", {"form": form, "action": "Create"})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, "Task updated!")
        return redirect("task_list")
    return render(request, "tasks/task_form.html", {"form": form, "action": "Update"})

@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.done = not task.done
    task.save()
    return redirect("task_list")

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted.")
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})
