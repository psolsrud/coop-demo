from django.db import models
from django.contrib.auth.models import AbstractUser

class DataModel(models.Model):
    geom = models.TextField(blank=True, null=True)
    speed = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    digital_tv = models.CharField(max_length=255, blank=True, null=True)
    home_autom = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data'

class DataDetailModel(models.Model):
    a_1 = models.CharField(max_length=255, blank=True, null=True)
    a_2 = models.CharField(max_length=255, blank=True, null=True)
    b_1 = models.CharField(max_length=255, blank=True, null=True)
    b_2 = models.CharField(max_length=255, blank=True, null=True)
    c_1 = models.CharField(max_length=255, blank=True, null=True)
    c_2 = models.CharField(max_length=255, blank=True, null=True)
    d_1 = models.CharField(max_length=255, blank=True, null=True)
    d_2 = models.CharField(max_length=255, blank=True, null=True)
    e_1 = models.CharField(max_length=255, blank=True, null=True)
    e_2 = models.CharField(max_length=255, blank=True, null=True)

    geom = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'data_detail'

class CustomUser(AbstractUser):
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)