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

from django.contrib.auth import authenticate, login, logout



import json, uuid, random, string, stripe, urllib, re



class test_my_acc(TestCase):

    def setUp(self):
        l = LawSociety(name='toast', eligibility ='Good', overview ='VGood', website='bomb.com')
        l.save()
        email = 'testy@testosterone.ca'
        password = hashers.make_password("password")

        profile = AppUser.create(first_name='test',last_name='tested', email=email, password=password,terms=True, society=l.pk)
        user = User.objects.get(username=email)
        profile.stripe_id = 'cus_6lp6xydAhnnT0F'
        user.is_active = True
        user.save()
        profile.save()



    def test_my_acc_index(self):
        c = Client()
        login = c.login(username='testy@testosterone.ca', password='password')
        resp = c.get('/user/options/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_change_email(self):
        c = Client()
        email = 'testy@testosterone.ca'
        login = c.login(username=email, password='password')
        resp = c.get('/user/options/', follow=True)
        self.assertEqual(resp.status_code, 200)

        # true cases
        resp = c.post('/user/options/email', {'email': email, 'email_confirm': email})
        user = User.objects.get(username=email)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(user.username == email)


        # false cases
        false_cases = [{'email': 'test@test.ca', 'email_confirm': 'test@test.d'},
                 {'email': '', 'email_confirm': ''},
                 {'email': 'test@test', 'email_confirm': 'test@test'},
                 {'email': 'test.ca', 'email_confirm': 'test.ca'},
                 {'toast': 'toast', 'test': 'test'}]

        for case in false_cases:
            c.post('/user/options/email', case)
            user = User.objects.get(email=email)
            self.assertTrue(user != None)

    def test_change_pass(self):
        c = Client()
        email = 'testy@testosterone.ca'
        password = 'password'

        c.login(username=email, password=password)
        resp = c.get('/user/options/')
        self.assertEqual(resp.status_code, 200)

        # true cases
        resp = c.post('/user/options/pass', {'pass_old': password, 'password_new': 'password1', 'vpass': 'password1'})
        password = 'password1'
        c.login(username=email, password=password)
        user = authenticate(username=email, password=password)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(user is not None)


        # false cases
        false_cases = [{'pass_old': 'email', 'password_new': 'password', 'vpass': 'password'},
                 {'pass_old': password, 'password_new': 'passwordfghf1', 'vpass': 'password'},
                 {'pass_old': password, 'password_new': 'pass', 'vpass': 'pass'},
                 {'pass_old': password, 'password_new': '', 'vpass': ''},
                 {'old': 'email', 'password_new': 'password', 'ass': 'password'}]

        login = c.login(username='testy@testosterone.ca', password='password')
        for case in false_cases:
            c.post('/user/options/pass', case)
            user = authenticate(username=email, password=case['password_new'])
            self.assertTrue(user is None)

        c.post('/user/options/pass', {'pass_old': password, 'password_new': 'password', 'vpass': 'password'})
