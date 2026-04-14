#!/usr/bin/env python3
"""
Django Web Application with Authentication — Auto-Setup Script
Generates the full project structure, then prints run instructions.

Usage:
    python setup_django_app.py
    cd taskmanager_project
    python manage.py runserver
"""

import os
import textwrap

PROJECT = "taskmanager_project"
APP = "tasks"

FILES = {}

# ── manage.py ──
FILES[f"{PROJECT}/manage.py"] = """\
#!/usr/bin/env python
import os, sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskmanager_project.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
"""

# ── settings.py ─
FILES[f"{PROJECT}/taskmanager_project/__init__.py"] = ""
FILES[f"{PROJECT}/taskmanager_project/settings.py"] = """\
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-change-me-in-production-abc123xyz"
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tasks",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "taskmanager_project.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = "/tasks/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
LOGIN_URL = "/accounts/login/"
# Email backend for password reset (prints to console in dev)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
"""

# ── urls.py (project) ──
FILES[f"{PROJECT}/taskmanager_project/urls.py"] = """\
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", include("tasks.urls_auth")),
    path("tasks/", include("tasks.urls")),
    path("", RedirectView.as_view(url="/tasks/", permanent=False)),
]
"""

# ── tasks/models.py ───
FILES[f"{PROJECT}/{APP}/__init__.py"] = ""
FILES[f"{PROJECT}/{APP}/models.py"] = """\
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY = [("low","Low"),("medium","Medium"),("high","High")]
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority    = models.CharField(max_length=10, choices=PRIORITY, default="medium")
    done        = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    due_date    = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["done", "-created_at"]

    def __str__(self):
        return self.title
"""

# ── tasks/forms.py ────
FILES[f"{PROJECT}/{APP}/forms.py"] = """\
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model  = User
        fields = ["username", "email", "password1", "password2"]

class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = ["title", "description", "priority", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
"""

# ── tasks/views.py ─────────────────────────────────────────────────────────
FILES[f"{PROJECT}/{APP}/views.py"] = """\
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
"""

# ── tasks/urls.py ─
FILES[f"{PROJECT}/{APP}/urls.py"] = """\
from django.urls import path
from . import views

urlpatterns = [
    path("",           views.task_list,   name="task_list"),
    path("new/",       views.task_create, name="task_create"),
    path("<int:pk>/edit/",   views.task_update, name="task_update"),
    path("<int:pk>/toggle/", views.task_toggle, name="task_toggle"),
    path("<int:pk>/delete/", views.task_delete, name="task_delete"),
]
"""

FILES[f"{PROJECT}/{APP}/urls_auth.py"] = """\
from django.urls import path
from .views import register
urlpatterns = [path("", register, name="register")]
"""

# ── tasks/admin.py ──
FILES[f"{PROJECT}/{APP}/admin.py"] = """\
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ["title", "user", "priority", "done", "created_at"]
    list_filter   = ["done", "priority", "user"]
    search_fields = ["title", "user__username"]
"""

# ── templates ─────────────────────────────────────────────────────────────
BASE_TPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Task Manager{% endblock %}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; background: #f0f2f5; color: #222; }
    nav { background: #2563eb; color: #fff; padding: .75rem 1.5rem; display: flex; align-items: center; gap: 1rem; }
    nav a { color: #fff; text-decoration: none; font-weight: 500; }
    nav a:hover { text-decoration: underline; }
    nav .spacer { flex: 1; }
    .container { max-width: 860px; margin: 2rem auto; padding: 0 1rem; }
    .card { background: #fff; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,.1); padding: 1.5rem; margin-bottom: 1rem; }
    .btn { display: inline-block; padding: .4rem .9rem; border-radius: 5px; border: none; cursor: pointer; font-size: .9rem; text-decoration: none; }
    .btn-primary { background: #2563eb; color: #fff; }
    .btn-sm { padding: .25rem .6rem; font-size: .8rem; }
    .btn-danger { background: #dc2626; color: #fff; }
    .btn-success { background: #16a34a; color: #fff; }
    .btn-secondary { background: #6b7280; color: #fff; }
    input, select, textarea { width: 100%; padding: .5rem; border: 1px solid #d1d5db; border-radius: 5px; margin-top: .25rem; font-size: .95rem; }
    label { font-weight: 500; font-size: .9rem; }
    .form-group { margin-bottom: 1rem; }
    .messages { list-style: none; margin-bottom: 1rem; }
    .messages li { padding: .6rem 1rem; border-radius: 5px; background: #d1fae5; color: #065f46; margin-bottom: .4rem; }
    .badge { display: inline-block; padding: .2rem .5rem; border-radius: 99px; font-size: .75rem; font-weight: 600; }
    .badge-low { background: #d1fae5; color: #065f46; }
    .badge-medium { background: #fef9c3; color: #713f12; }
    .badge-high { background: #fee2e2; color: #991b1b; }
    .done-row { opacity: .5; text-decoration: line-through; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: .6rem .8rem; text-align: left; border-bottom: 1px solid #e5e7eb; }
    th { background: #f9fafb; font-size: .85rem; }
    .filters a { margin-right: .5rem; font-size: .9rem; }
  </style>
</head>
<body>
<nav>
  <a href="/tasks/"><strong>📋 Task Manager</strong></a>
  <div class="spacer"></div>
  {% if user.is_authenticated %}
    <span>👤 {{ user.username }}</span>
    <a href="/tasks/new/" class="btn btn-primary btn-sm">+ New Task</a>
    <form method="post" action="/accounts/logout/" style="display:inline">
      {% csrf_token %}<button class="btn btn-secondary btn-sm" type="submit">Logout</button>
    </form>
  {% else %}
    <a href="/accounts/login/">Login</a>
    <a href="/accounts/register/">Register</a>
  {% endif %}
</nav>
<div class="container">
  {% if messages %}
  <ul class="messages">{% for m in messages %}<li>{{ m }}</li>{% endfor %}</ul>
  {% endif %}
  {% block content %}{% endblock %}
</div>
</body>
</html>
"""

FILES[f"{PROJECT}/templates/base.html"] = BASE_TPL

FILES[f"{PROJECT}/templates/registration/login.html"] = """\
{% extends "base.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="card" style="max-width:420px;margin:auto">
  <h2 style="margin-bottom:1rem">Login</h2>
  <form method="post">{% csrf_token %}
    <div class="form-group"><label>Username</label>{{ form.username }}</div>
    <div class="form-group"><label>Password</label>{{ form.password }}</div>
    <button class="btn btn-primary" type="submit">Login</button>
    <a href="/accounts/register/" style="margin-left:1rem;font-size:.9rem">Register</a>
    <a href="/accounts/password_reset/" style="margin-left:1rem;font-size:.9rem">Forgot password?</a>
  </form>
</div>
{% endblock %}
"""

FILES[f"{PROJECT}/templates/registration/password_reset_form.html"] = """\
{% extends "base.html" %}
{% block title %}Reset Password{% endblock %}
{% block content %}
<div class="card" style="max-width:420px;margin:auto">
  <h2 style="margin-bottom:1rem">Reset Password</h2>
  <p style="margin-bottom:1rem;font-size:.9rem">Enter your email — a reset link will be printed to the console (dev mode).</p>
  <form method="post">{% csrf_token %}
    <div class="form-group"><label>Email</label>{{ form.email }}</div>
    <button class="btn btn-primary" type="submit">Send Reset Link</button>
  </form>
</div>
{% endblock %}
"""

FILES[f"{PROJECT}/templates/registration/password_reset_done.html"] = """\
{% extends "base.html" %}
{% block content %}
<div class="card" style="max-width:420px;margin:auto">
  <h2>Check your console</h2>
  <p style="margin-top:.8rem">In development mode, the password reset email is printed to the server console.</p>
</div>
{% endblock %}
"""

FILES[f"{PROJECT}/templates/registration/password_reset_confirm.html"] = """\
{% extends "base.html" %}
{% block title %}Set New Password{% endblock %}
{% block content %}
<div class="card" style="max-width:420px;margin:auto">
  <h2 style="margin-bottom:1rem">Set New Password</h2>
  <form method="post">{% csrf_token %}
    <div class="form-group"><label>New password</label>{{ form.new_password1 }}</div>
    <div class="form-group"><label>Confirm password</label>{{ form.new_password2 }}</div>
    <button class="btn btn-primary" type="submit">Set Password</button>
  </form>
</div>
{% endblock %}
"""

FILES[f"{PROJECT}/templates/registration/password_reset_complete.html"] = """\
{% extends "base.html" %}
{% block content %}
<div class="card" style="max-width:420px;margin:auto">
  <h2>Password Reset Complete</h2>
  <p style="margin-top:.8rem"><a href="/accounts/login/">Login with your new password →</a></p>
</div>
{% endblock %}
"""

FILES[f"{PROJECT}/templates/tasks/register.html"] = """\
{% extends "base.html" %}
{% block title %}Register{% endblock %}
{% block content %}
<div class="card" style="max-width:420px;margin:auto">
  <h2 style="margin-bottom:1rem">Create Account</h2>
  <form method="post">{% csrf_token %}
    {% for field in form %}
    <div class="form-group">
      <label>{{ field.label }}</label>{{ field }}
      {% if field.errors %}<p style="color:#dc2626;font-size:.8rem">{{ field.errors.0 }}</p>{% endif %}
    </div>
    {% endfor %}
    <button class="btn btn-primary" type="submit">Register</button>
    <a href="/accounts/login/" style="margin-left:1rem;font-size:.9rem">Already have an account?</a>
  </form>
</div>
{% endblock %}
"""

FILES[f"{PROJECT}/templates/tasks/task_list.html"] = """\
{% extends "base.html" %}
{% block title %}My Tasks{% endblock %}
{% block content %}
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem">
  <h2>My Tasks</h2>
  <div class="filters">
    <a href="?filter=all" {% if filter_by == "all" %}style="font-weight:700"{% endif %}>All</a>
    <a href="?filter=pending" {% if filter_by == "pending" %}style="font-weight:700"{% endif %}>Pending</a>
    <a href="?filter=done" {% if filter_by == "done" %}style="font-weight:700"{% endif %}>Done</a>
  </div>
</div>
{% if tasks %}
<div class="card" style="padding:0">
<table>
  <thead><tr><th>Title</th><th>Priority</th><th>Due</th><th>Actions</th></tr></thead>
  <tbody>
  {% for task in tasks %}
  <tr class="{% if task.done %}done-row{% endif %}">
    <td>{{ task.title }}<br><small style="color:#6b7280">{{ task.description|truncatechars:60 }}</small></td>
    <td><span class="badge badge-{{ task.priority }}">{{ task.get_priority_display }}</span></td>
    <td>{{ task.due_date|default:"—" }}</td>
    <td style="white-space:nowrap">
      <form method="post" action="/tasks/{{ task.pk }}/toggle/" style="display:inline">{% csrf_token %}
        <button class="btn btn-sm {% if task.done %}btn-secondary{% else %}btn-success{% endif %}" type="submit">
          {% if task.done %}Undo{% else %}Done{% endif %}
        </button>
      </form>
      <a href="/tasks/{{ task.pk }}/edit/" class="btn btn-sm btn-primary">Edit</a>
      <a href="/tasks/{{ task.pk }}/delete/" class="btn btn-sm btn-danger">Del</a>
    </td>
  </tr>
  {% endfor %}
  </tbody>
</table>
</div>
{% else %}
<div class="card"><p>No tasks yet. <a href="/tasks/new/">Create one →</a></p></div>
{% endif %}
{% endblock %}
"""

FILES[f"{PROJECT}/templates/tasks/task_form.html"] = """\
{% extends "base.html" %}
{% block title %}{{ action }} Task{% endblock %}
{% block content %}
<div class="card" style="max-width:540px;margin:auto">
  <h2 style="margin-bottom:1rem">{{ action }} Task</h2>
  <form method="post">{% csrf_token %}
    {% for field in form %}
    <div class="form-group">
      <label>{{ field.label }}</label>{{ field }}
      {% if field.errors %}<p style="color:#dc2626;font-size:.8rem">{{ field.errors.0 }}</p>{% endif %}
    </div>
    {% endfor %}
    <button class="btn btn-primary" type="submit">{{ action }}</button>
    <a href="/tasks/" class="btn btn-secondary" style="margin-left:.5rem">Cancel</a>
  </form>
</div>
{% endblock %}
"""

FILES[f"{PROJECT}/templates/tasks/task_confirm_delete.html"] = """\
{% extends "base.html" %}
{% block title %}Delete Task{% endblock %}
{% block content %}
<div class="card" style="max-width:420px;margin:auto">
  <h2>Delete "{{ task.title }}"?</h2>
  <p style="margin:.8rem 0">This action cannot be undone.</p>
  <form method="post">{% csrf_token %}
    <button class="btn btn-danger" type="submit">Yes, delete</button>
    <a href="/tasks/" class="btn btn-secondary" style="margin-left:.5rem">Cancel</a>
  </form>
</div>
{% endblock %}
"""

# ── requirements.txt ──
FILES[f"{PROJECT}/requirements.txt"] = "django>=4.2\n"

# ── Write all files ───
def write_files():
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(textwrap.dedent(content))
    print(f" Created {len(FILES)} files in ./{PROJECT}/")


# ── Run migrations automatically ────
def run_setup():
    import subprocess
    mgr = f"{PROJECT}/manage.py"
    print("\nRunning migrations...")
    subprocess.run(["python", mgr, "migrate"], check=True)
    print("\n Database ready.")
    print("""
    """)


if __name__ == "__main__":
    write_files()
    run_setup()