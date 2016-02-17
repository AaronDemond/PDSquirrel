__author__ = 'Aaron'
from django.db import models
from django.contrib.auth.models import User
from pds_v3.v_functions import clean_join,accept_input




class AppUserManager(models.Manager):

    def create_presenter(self,):
        user = self.is_presenter = True
        user.save()
