from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='pics')
    avr_score = models.PositiveIntegerField(null=True, blank=True)
    tests_list_passed = models.PositiveIntegerField(null=True, blank=True)
