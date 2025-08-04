from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    """Todo model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title