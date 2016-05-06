from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import  hashers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from pds_v3.models import PdSession, AppUser, LawSociety, LawSocietyOverride, Purchase
from django.core.mail import send_mail
from django.contrib import messages
from pds_v3.forms import CaptchaForm
from pds_v3.forms import PdSessionForm

from django.test import TestCase, Client


import json, uuid, random, string, stripe, urllib, re



class test_my_acc(TestCase):

    def setUp(self):
        l = LawSociety(name='toast', eligibility ='Good', overview ='VGood', website='bomb.com')
        l.save()
        email = 'testy@testosterone.ca'
        password = hashers.make_password("password")
        profile = AppUser.create(first_name='test',last_name='tested', email=email,
                              password=password,terms=True, society=1)
        user = User.objects.get(username=email)
        profile.stripe_id = 'cus_6lp6xydAhnnT0F'
        user.is_active = True
        user.save()
        profile.save()


    def test_index(self):

        c = Client()
        login = c.login(username='testy@testosterone.ca', password='password')
        resp = c.get('/user/options/', follow=True)
        self.assertEqual(resp.status_code, 200)
