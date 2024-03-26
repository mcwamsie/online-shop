import email
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=255,
        choices=[
        ('M', 'MALE'),
        ('F', 'FEMALE')
    ])

    REQUIRED_FIELDS = [
        'email',
        'password',
        'first_name',
        'last_name',
        'date_of_birth',
        'gender'
    ]
