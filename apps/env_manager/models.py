from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Environment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='environments', null=True, blank=True)
    
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='stopped')
    resource_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class EnvironmentTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name