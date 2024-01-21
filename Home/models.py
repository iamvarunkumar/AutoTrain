from django.db import models
from django.contrib.auth.models import User

class UserSignUpDetails(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    rep_password = models.CharField(max_length=255)
    account_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"