__author__ = 'Aaron'
from django.db import models
from django.contrib.auth.models import User




class AppUserManager(models.Manager):

    def create_presenter(self,):
        user = self.is_presenter = True
        user.save()
