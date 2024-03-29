from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    about = models.TextField(null=True)
