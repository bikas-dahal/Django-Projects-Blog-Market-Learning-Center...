# models.py
from django.db import models
from django.contrib.auth.models import User

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction for {self.user.username} at {self.timestamp}"
