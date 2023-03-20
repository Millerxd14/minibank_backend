from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Cuenta(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    n_cuenta = models.CharField(max_length=25)
    saldo = models.IntegerField()

    created         = models.DateTimeField(auto_now_add=True)
    modified        = models.DateTimeField(auto_now = True)
