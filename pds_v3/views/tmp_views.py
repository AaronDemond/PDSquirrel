__author__ = 'Aaron'

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from pds_v3.models import PdSession, AppUser, LawSociety, LawSocietyOverride, Purchase
from pds_v3.forms import CaptchaForm
from pds_v3 import tasks


def about(request):
    return render(request, 'v3/final/learn.html')

def terms(request):
    return render(request, 'v3/final/terms.html')

def privacy(request):
    return render(request, 'v3/final/privacy.html')

def become_presenter(request):
    return render(request, 'v3/final/become-presenter.html')


def contact(request):

    if 'from_pres' in request.GET:
        c = {'from_pres': True}
    else:
        c = {'from_pres': 'False'}
    return render(request, 'v3/final/contact.html', c)

def support_msg(request):
    if request.POST:
        email = request.POST['user_email']
        name = request.POST['name']
        message = request.POST['message']
        subject = request.POST['subject']

        subject = 'PDSquirrel support from  ' + name + ' subj: ' + subject
        send_to = ['admin@pdsquirrel.ca']
        msg = message + '\nreturn email: ' + email

        tasks.sendMail.apply_async([send_to, subject, msg])

        #send_mail('PDSquirrel support from  ' + name + ' subj: ' + subject , message + '\nreturn email: ' + email , 'support@pdsquirrel.ca', ['admin@pdsquirrel.ca'], fail_silently=False)

        messages.success(request, 'Message sent. We will get back to you shortly')
        return render(request, 'v3/final/contact.html')

    else:
        return HttpResponseRedirect('/contact/')

def cap_ajax(request):
    form = CaptchaForm()
    c = Context({'form':form})
    t = Template("{{form.captcha}}")
    page = t.render(c)
    return HttpResponse(page)
