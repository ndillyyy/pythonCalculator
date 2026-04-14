from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ["title", "user", "priority", "done", "created_at"]
    list_filter   = ["done", "priority", "user"]
    search_fields = ["title", "user__username"]
