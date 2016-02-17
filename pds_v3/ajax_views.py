from django.shortcuts import render, HttpResponse
from pds_v3.models import PdSession, AppUser, LawSociety, LawSocietyOverride, Purchase,\
Subject, PdAudio
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def echo_status(request):
    context = {'msg' : "it works!"}
    return context

def ajax_test(request):
    subjects = Subject.objects.all()
    recordings = PdAudio.objects.filter(appuser = request.user.profile, used = False, hidden = False)
    context = {'subjects' : subjects, 'recordings' : recordings}
    return render(request, 'v3/final/presenter-pages/final/upload.html', context)
    return HttpResponse("This is a response")
