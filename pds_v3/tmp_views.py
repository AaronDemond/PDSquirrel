__author__ = 'Aaron'

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from pds_v3.models import PdSession, AppUser, LawSociety, LawSocietyOverride, Purchase

def about(request):
    return render(request, 'v3/final/about.html')

def learn(request):
    return render(request, 'v3/final/learn.html')

def contact(request):

    if 'from_pres' in request.GET:
	c = {'from_pres': True}
    else:
	c = {'from_pres': 'False'}
    return render(request, 'v3/final/contact.html', c)


def terms(request):
    return render(request, 'v3/final/terms.html')

def presenter_terms(request):
    return render(request, 'v3/final/terms-presenter.html')
def privacy(request):
    return render(request, 'v3/final/privacy.html')
def become_presenter(request):
    return render(request, 'v3/final/become-presenter.html')





from pds_v3.forms import CaptchaForm
def cap(request):

    if request.POST:
        f = CaptchaForm(request.POST)


        if f.is_valid():
            return HttpResponse("True!!")
        else:
            return HttpResponse("False!!")
    else:
        context = {'form':CaptchaForm}
        return render(request, 'v3/final/cap.html', context)

def cap_ajax(request):
    form = CaptchaForm()
    c = Context({'form':form})
    t = Template("{{form.captcha}}")
    page = t.render(c)
    return HttpResponse(page)
