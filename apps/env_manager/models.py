from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Environment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='environments')
    
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='stopped')
    resource_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name