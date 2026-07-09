from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=140)
    done = models.BooleanField(default=False)
    due_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title