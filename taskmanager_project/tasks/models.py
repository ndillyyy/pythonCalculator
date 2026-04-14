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
