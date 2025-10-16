from django.db import models
from django.conf import settings

class Task(models.Model):
    status_labels = [
        ('pending', 'Pending'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks') #task linked to logged in user
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_labels, default='pending')
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
