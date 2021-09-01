
# Create your models here.
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser,User
import datetime
from django.utils import timezone
from simple_history.models import HistoricalRecords

# Create your models here.


class ButtonCalls(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stupid = models.IntegerField(blank=True, null=True)
    fat = models.IntegerField(blank=True, null=True)
    dumb = models.IntegerField(blank=True, null=True)
