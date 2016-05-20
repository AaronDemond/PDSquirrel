from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from itertools import chain
import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pds_v3.models import PdSession, AppUser, LawSociety, LawSocietyOverride, Purchase, Subject, Presenter
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template import Context, Template
import pdb; #pdb.set_trace()
import json
from pds_v3.forms import CaptchaForm
import stripe


#only root level url
def landing(request):
    content = PdSession.objects.order_by('name')[0:4]
    presenter = Presenter.objects.order_by('date_approved')[0:2]
    context = {
        'presenter': presenter,
        'content': content
    }
    return render(request, 'v3/final/home.html', context)


def membership_information(request):
    return render(request, 'v3/final/membership-info.html')




def browse(request):
    #pdb.set_trace()

    if request.POST:
        query = request.POST.get('query', None)
        subject = request.POST.get('subject', None)
        if subject != None:
            if subject == '0':
                sub_name = 'All Subjects'
            else:
                sub_name = Subject.objects.get(pk=subject)
        else:
            sub_name = None


        search_type = request.POST.get('search_type', None)

        if search_type == 'search':
            users_queried = User.objects.filter(first_name__icontains=query)
            presenters_queried = Presenter.objects.filter(user__in=users_queried)
            list_by_presenter = PdSession.objects.filter(presenters__in=presenters_queried, approved=True, suspended=False, archived=False).order_by('-upload_date')
            tmplist = PdSession.objects.filter(description__icontains=query, approved=True, suspended=False, archived=False).order_by('-upload_date')
            tmplist2 = PdSession.objects.filter(name__icontains=query, approved=True, suspended=False, archived=False).order_by('-upload_date')
            pdlist = list(set(chain(tmplist, tmplist2, list_by_presenter))) #chain together, get rid of duplicates by constructing a set, convert to list for template

        else:
            if subject == '0':
                pdlist = PdSession.objects.filter(approved=True, suspended=False, archived=False).order_by('-upload_date')
            else:
                pdlist = PdSession.objects.filter(subject=subject, approved=True, suspended=False, archived=False).order_by('-upload_date')

        if pdlist:

            paginator = Paginator(pdlist, 10)
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
            page_range = range(1,pd.paginator.num_pages + 1)
        else:
            page_range = range(False)

    else:
        pd_list = PdSession.objects.all()
        pd_list = PdSession.objects.filter(approved=True, suspended=False, archived=False).order_by('-upload_date')
        if pd_list:
            paginator = Paginator(pd_list, 10)

            page = request.GET.get('page')
            try:
                pd = paginator.page(page)
            except PageNotAnInteger:
                pd = paginator.page(1)
            except EmptyPage:
                pd = paginator.page(paginator.num_pages)
        search_type = 'search'



        if pd_list:
            page_range = range(1,pd.paginator.num_pages + 1)
        else:
            pd = False
            page_range = range(False)

        context =  {'pd_list' : pd, 'subjects' : Subject.objects.all(), 'type' : search_type, 'range' :  page_range, 'subject' : 'All Subjects',}
        return render(request, 'v3/final/browse.html' , context)


    return render(request, 'v3/final/browse.html' , {'pd_list' : pd, 'range' : page_range, 'subjects' : Subject.objects.all(), 'type' : search_type, 'subject' : sub_name, 'query' : query})


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
def fuseEdit(edit,pd):
    pd.name=edit.name
    pd.description=edit.description

    for attachment in edit.attachments.all():
        pd.attachments.add(attachment)

    if edit.audio_file:
        pd.audio_file = edit.audio_file

    pd.subject.clear()
    for subject in edit.subjects.all():
        pd.subject.add(subject)
    return pd

def preview(request,id):
    session = PdSession.objects.get(pk=id)
    presenter = Presenter.objects.filter(user=request.user)[0]


    if session in presenter.pdsession_set.all():
        context = {'pd': session, 'preview' : True, 'presenter' : presenter}
    else:
        return HttpResponse('auth error')
    if 'l' in request.GET:
        messages.add_message(request, messages.INFO, 'Click to listen the PD Session shown below.')
        return render(request, 'v3/final/presenter-pages/final/preview.html', context)


    if session.edited == True:
        edit = session.edits.order_by('-date')[0]
        context['edit'] = edit
        session.name = edit.name
        session.description = edit.description
        messages.add_message(request, messages.INFO, 'Click to preview the PD Session shown below.')
    else:
        if session.approved:
            messages.add_message(request, messages.INFO, 'Click to preview the PD Session shown below.')
        else:
            messages.add_message(request, messages.INFO, 'Click to preview the PD Session shown below.')

    return render(request, 'v3/final/presenter-pages/final/preview.html', context)

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

    context = {'pd' : pd, 'own' : own}

    if request.user.is_authenticated():
        context['customer'] = stripe.Customer.retrieve(request.user.profile.stripe_id)

    return render(request, 'v3/final/detail.html', context )





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

    if profile.bio == '':
        messages.info(request, 'This presenter has not completed their Biography page yet, check again soon.')
        return HttpResponseRedirect('/browse/')

    name = profile
    context = {'name': name, 'bio': profile.bio, 'img': '/static/img/placeholder.png ', 'presenter': profile}
    return render(request, 'v3/final/presenter-landing.html', context)



def watch(request, pd_id):
    pd = PdSession.objects.get(pk=pd_id)
    context = {'pd': pd}

    #if user owns pd, show them and mark as 'complete' (viewed)
    for x in request.user.profile.purchase_set.all():
        if x.pdsession == pd:
            x.completed = True; x.save()
            return render(request, 'v3/final/view.html', context)

    #if its a presenter, they may be previewing
    if request.user.profile.is_presenter:
        presenter = Presenter.objects.get(user=request.user)
        if presenter in pd.presenters.all():
            return render(request, 'v3/final/view.html', context)

    return HttpResponse('Invalid Request')

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
        email = request.POST['user_email']
        name = request.POST['name']
        message = request.POST['message']
        subject = request.POST['subject']

        #email = EmailMessage('Testing Email instance','body test message', 'support@pdsquirrel.ca',['admin@pdsquirrel.ca'],
                #['demondsoftware@gmail.com'])
        send_mail('PDSquirrel support from  ' + name + ' subj: ' + subject , message + '\nreturn email: ' + email , 'support@pdsquirrel.ca', ['admin@pdsquirrel.ca'], fail_silently=False)


        messages.success(request, 'Message sent. We will get back to you shortly')
        return render(request, 'v3/final/contact.html')

    else:
        return HttpResponseRedirect('/contact/')




def upload_admin(request, pd_id=False):
    c = {}
    #Must be an ADMIN
    if request.user.is_superuser == True:

        #Make changes to sessions
        if request.POST:
            pd = PdSession.objects.get(pk=request.POST['pd'])
            if "approve" in request.POST:
                if pd.suspend_request == True:
                    pd.suspended = True

                if pd.edited:
                    edit = pd.edits.latest('date')
                    pd = fuseEdit(edit,pd)

                    for attachment in pd.attachments.all():
                        if attachment.mark_for_delete == True:
                            attachment.delete()

                pd.price = 9.99
                pd.edited=False
                pd.approved = True
                now = datetime.datetime.now()
                pd.release_date = now
                pd.save()
                messages.success(request, 'Session Approved')

        #if pd number is provided, half of page is rendered with a session to review
        if pd_id:
            pd = PdSession.objects.get(pk=pd_id)
            if pd.edited:
                edit = pd.edits.latest('date')
                c['edit'] = edit
            c['pd'] = pd
            return render(request, 'v3/final/myadmin/session.html', c)


        c["unapproved_pd"] = PdSession.objects.filter(approved=False, presenter_approved=True,
                suspended=False, suspend_request=False)
        c["edited_pd"] = PdSession.objects.filter(edited=True, presenter_approved=True,
                approved=True, suspended=False, suspend_request=False)
        c['removed_pd'] = PdSession.objects.filter(suspend_request=True, suspended=False)
        return render(request, 'v3/final/myadmin/uploads.html', c)

    #if not an admin
    return HttpResponse('Invalid Credentials')

def accounting_admin(request):
    return render(request, 'v3/final/myadmin/accounting.html')
