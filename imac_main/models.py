from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField(max_length=500, unique=True)
    uid = models.CharField(max_length=500, unique=True)
    name = models.CharField(max_length=500)
    acc_type = models.CharField(max_length=500)

    def __str__(self):
        return self.email