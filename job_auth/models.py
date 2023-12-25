from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    company_id = models.ImageField(upload_to='company_id/', blank=True, null=True)

    def __str__(self):
        return str(self.user)