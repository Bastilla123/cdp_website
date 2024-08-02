from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    loglevel = models.CharField(max_length=1,default="")
    text = models.TextField(default="")