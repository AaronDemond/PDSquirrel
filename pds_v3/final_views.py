from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from pds_v3.models import PdSession, AppUser, LawSociety, LawSocietyOverride, Purchase, Subject
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'v3/final/home.html')
