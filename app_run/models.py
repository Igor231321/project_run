from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):
    class Status(models.TextChoices):
        INIT = 'init', 'init'
        IN_PROGRESS = 'in_progress', 'in_progress'
        FINISHED = 'finished' 'finished'

    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    status = models.CharField(max_length=25, choices=Status, default=Status.INIT)

    def __str__(self):
        return self.comment