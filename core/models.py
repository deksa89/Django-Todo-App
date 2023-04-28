from django.db import models
from django.contrib.auth.models import User


class Errand(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['completed']
    