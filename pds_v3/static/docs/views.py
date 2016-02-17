from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pds_v3.models import PdSession, AppUser, LawSociety, LawSocietyOverride, Purchase, Subject
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template import Context, Template
import pdb; #pdb.set_trace()
import json
from pds_v3.forms import CaptchaForm
#only root level url
def landing(request):
    pd_list = PdSession.objects.all()
    context = {'pd_list': pd_list}
    return render(request, 'v3/final/home.html', context)




#any url prefixed with pd/
def browse(request):
    #pdb.set_trace()

    #import pdb; pdb.set_trace()
    if request.POST:
        query = request.POST.get('query', None)
        subject = request.POST.get('subject', None)
        search_type = request.POST.get('search_type', None)

        if search_type == 'search':
            pdlist = PdSession.objects.filter(description__contains=query, approved=True, suspended=False, archived=False).order_by('-release_date')
        else:
            if subject == '0':
                pdlist = PdSession.objects.filter(approved=True, suspended=False, archived=False).order_by('-release_date')
            else:
                pdlist = PdSession.objects.filter(subject=subject, approved=True, suspended=False, archived=False).order_by('-release_date')

        if pdlist:

            paginator = Paginator(pdlist, 6)
            page = request.GET.get('page')
            try:
                pd = paginator.page(page)
            except PageNotAnInteger:
                pd = paginator.page(1)
            except EmptyPage:
                pd = paginator.page(paginator.num_pages)
        else:
            pd = False

        if pd:
            page_range = pd.paginator.num_pages + 1
        else:
            page_range = 0

    else:
        pd_list = PdSession.objects.all()
        pd_list = PdSession.objects.filter(approved=True, suspended=False, archived=False).order_by('-release_date')
        if pd_list:
            paginator = Paginator(pd_list, 6)

            page = request.GET.get('page')
            try:
                pd = paginator.page(page)
            except PageNotAnInteger:
                pd = paginator.page(1)
            except EmptyPage:
                pd = paginator.page(paginator.num_pages)
        else:
            pd = False
        search_type = 'browse'



        if pd:
            page_range = pd.paginator.num_pages + 1
        else:
            page_range = 0


        context =  {'pd_list' : pd, 'subjects' : Subject.objects.all(), 'type' : search_type, 'range' :  page_range}
        return render(request, 'v3/final/browse.html' , context)


    return render(request, 'v3/final/browse.html' , {'pd_list' : pd, 'range' : page_range, 'subjects' : Subject.objects.all(), 'type' : search_type, 'subject' : subject, 'query' : query})


def place_holder(request):
    return HttpResponse('placeholder')

def activate(request, id):
	user_id = id - 9
	user = AppUser.objects.get(pk=user_id)
	user.is_active = 1
	user.save()
	return HttpResponse("activated")



def debug(request):
    return render(request, 'v3/debug-django.html')

def email(request):
	msg = "Please go to the following link to activate: http://pdsquirrel.ca:90/activate/" + str(request.user.id) + "/"
	try:
		send_mail('PD Squirrel Activation', msg, 'no-reply@pdsquirrel.ca',['demondsoftware@gmail.com'], fail_silently=False)
	except:
		return HttpResponse("email not sent")

	return HttpResponse("Email sent")

def learn(request):
    return HttpResponse("empty learning page")

def cap_refresh(request):
    form = CaptchaForm()
    c = Context({'form':form})
    t = Template("{{form.captcha}}")
    page = t.render(c)
    return HttpResponse(page)

def detail(request, pd_id):
    pd = PdSession.objects.get(pk=pd_id)
    if request.user.is_authenticated():
        user_pd = Purchase.objects.filter(user=request.user.profile)
        own = 0
        for x in user_pd:
            if pd == x.pdsession:
                own = 1
    else:
        own = 0
    return render(request, 'v3/final/detail.html', {'pd' : pd, 'own' : own})





#should return a dict containing society name, eligibility, and overview based on given PD.
def getSocietyPdInfo(pd_id,society_id):

    pd = PdSession.objects.get(pk=pd_id)
    given_society = LawSociety.objects.get(pk=society_id)
    overrides = pd.lawsocietyoverrides.all()


    result = {}


    #loop through all overrides attached to pd. If any of their society obj matches the given soc obj, return that
    #information. Otherwise, use the default.
    for override in overrides:
        if override.parent == given_society:
            result['eligibility'] = override.eligibility
            result['overview'] = override.parent.overview
            result['name'] = override.parent.name
            return result

    #if nothing found in overrides, return the default.
    result['eligibility'] = given_society.eligibility
    result['overview'] = given_society.overview
    result['name'] = given_society.name
    return result




def accred(request, pd_id, s_id=1):
    pd = PdSession.objects.get(pk=pd_id)
    societies = LawSociety.objects.all()
    context = { 'pd': pd, 'societies': societies}

    #means no society passed in url, use user society. if not logged, use def of 0.
    if request.user.is_authenticated():
        context['society_default'] = request.user.profile.society.all()[0]
        context['society_chosen'] = LawSociety.objects.get(pk=s_id)
        result = getSocietyPdInfo(pd_id, s_id)

    else:
        result = getSocietyPdInfo(pd_id, s_id)
        context['society_chosen'] = LawSociety.objects.get(pk=s_id)

    context['eligibility'] = result['eligibility']
    context['overview'] = result['overview']


    return render(request, 'v3/final/accred.html', context)




from pds_v3 import models
def presenter_detail(request, p_id):
    profile = models.Presenter.objects.get(id=p_id)
    name = profile
    context = {'name': name, 'bio': profile.bio, 'img': '/static/img/placeholder.png ', 'presenter': profile}
    return render(request, 'v3/final/presenter-landing.html', context)



def watch(request, pd_id):
    pd = PdSession.objects.get(pk=pd_id)
    context = {'pd': pd}
    return render(request, 'v3/final/view.html', context)

from .forms import UploadFileForm



#takes a file input in the form request.FILES['input-name'] and uploads ti to the abs path specified.
#not sure about priveliges.
def handle_uploaded_file(f):
    path = f.name
    name = f.name
    dest = open('/root/nginx/pds/' + name, 'w')
    for chunk in f.chunks():
        dest.write(chunk)
    dest.close()

def upload(request):
    if request.POST:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['audio_file'])
            return HttpResponse("SUCCESS")
        else:
            return HttpResponse(form.errors)
    else:
        return render(request, 'v3/final/upload.html')


def download_example(request):
    return HttpResponse


from django.core.mail import send_mail
def support_msg(request):
    if request.POST:
        email = request.POST['email']
        name = request.POST['name']
        subject = request.POST['subject']
        message = request.POST['message']

        send_mail('support', message, 'support@pdsquirrel.ca', ['demondsoftware@gmail.com'], fail_silently=False)
        return HttpResponse("mail sent")

    else:
        return HttpResponseRedirect('/contact/')












