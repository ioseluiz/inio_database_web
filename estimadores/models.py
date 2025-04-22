from django.db import models

class Estimador(models.Model):
    name = models.CharField(max_length=50)
    initials = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.initials}"
    
    class Meta:
        ordering = ['-created_at']
