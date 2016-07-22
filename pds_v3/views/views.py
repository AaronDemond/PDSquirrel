from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
import os
from itertools import chain
import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pds_v3.models import PdSession, AppUser, LawSociety, LawSocietyOverride, Purchase, Subject, Presenter, PdAttachment, Comment, PdAudio
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template import Context, Template, RequestContext
import pdb #pdb.set_trace()
import json
from pds_v3 import tasks
from pds_v3.forms import CaptchaForm
import stripe


#only root level url
def landing(request):

    # Newest 4 Sessions should appear on the home page
    pd = PdSession.objects.filter(approved=True, suspended=False, archived=False).order_by('-upload_date')
    pd = list(pd)
    content = pd[:4]
    subjects = Subject.objects.all()

    context = {
        'content': content,
        'subjects': subjects
    }
    return render(request, 'v3/final/home.html', context)


def browse(request):
    search_type = request.GET.get('search_type', None)
    if search_type == 'browse' or search_type == 'search':
        query = request.GET.get('query', None)
        subject = request.GET.get('subject', None)
        if subject != None:
            if subject == '0':
                sub_name = 'All Subjects'
            else:
                sub_name = Subject.objects.get(pk=subject)
        else:
            sub_name = None

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


def getAttachment(request, a_id):
    '''
    Returns a link to attachments of a pdsession, if the user has the rights.
    '''
    attachment = PdAttachment.objects.get(id=a_id)
    pd = attachment.pdsession_set.all()[0]

    owned_sessions = [purchase.pdsession for purchase in request.user.profile.purchase_set.all()]
    if request.user.profile.is_presenter == True:
        created_sessions = request.user.presenter.pdsession_set.all()
        owned_sessions = list(chain(created_sessions, owned_sessions))

    if pd in owned_sessions or request.user.is_superuser:
        name = attachment.filename()
        response = HttpResponse()
        response["Content-Disposition"] = "attachment; filename={0}".format(name)
        response['X-Accel-Redirect'] = "/attachments/{0}".format(name)
        return response

    return HttpResponse('error')

def getRecordingWav(request, audio_id):
    pdaudio = PdAudio.objects.get(pk=audio_id)
    owned_recordings = request.user.profile.pdaudio_set.all()
    if pdaudio in owned_recordings or request.user.is_superuser:
        name = os.path.basename(pdaudio.audio.name)

    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename={0}".format(name)
    response['X-Accel-Redirect'] = "/content/{0}".format(name)
    return response

def getRecordingMp3(request, audio_id):
    '''
    If a presenter owns a recording, a link to the mp3 will be returned.
    '''
    pdaudio = PdAudio.objects.get(pk=audio_id)
    owned_recordings = request.user.profile.pdaudio_set.all()
    if pdaudio in owned_recordings or request.user.is_superuser:
        name = os.path.basename(pdaudio.getMp3Location())

        response = HttpResponse()
        response["Content-Disposition"] = "attachment; filename={0}".format(name)
        response['X-Accel-Redirect'] = "/content/{0}".format(name)
        return response


def getAudio(request, pd_id):
    '''
    Returns link to mp3 of pdsession
    '''

    pd = PdSession.objects.get(pk=pd_id)

    if pd.pdaudio:
        name = os.path.basename(pd.getAudioLocation())
    else:
        name = os.path.basename(pd.getAudioLocation().url)

    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename={0}".format(name)
    response['X-Accel-Redirect'] = "/content/{0}".format(name)
    return response


def detail(request, pd_id):

    pd = PdSession.objects.get(pk=pd_id)
    comments = Comment.objects.filter(pd_id = pd_id, parent__isnull = True).order_by('-date')
    own = 0
    context = {'pd' : pd, 'comments': comments}
    context['url'] = "pd/"+pd_id

    if request.user.is_authenticated():
        owned_sessions = [purchase.pdsession for purchase in request.user.profile.purchase_set.all()]
        if request.user.profile.is_presenter == True:
            created_sessions = request.user.presenter.pdsession_set.all()
            owned_sessions = list(chain(created_sessions, owned_sessions))

        if pd in owned_sessions or request.user.is_superuser:
            own = 1

        if own == 0:
            messages.info(request, 'During our initial beta release, only sessions you\'ve created can be listened to. This session will be available for purchase at a later date. Check back soon!')

        context['customer'] = stripe.Customer.retrieve(request.user.profile.stripe_id)


    context['own'] = own

    if pd.suspended == True and own == 0:
        return HttpResponse("This session has been removed. Only users who have purchased the rights may access it.");

    return render(request, 'v3/final/detail.html', context)



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
    presenter = models.Presenter.objects.get(id=p_id)

    if presenter.bio == '':
        messages.info(request, 'This presenter has not completed their Biography page yet, check again soon.')
        return HttpResponseRedirect('/browse/')

    name = presenter
    context = {'name': name, 'bio': presenter.bio, 'img': '/static/img/placeholder.png ', 'presenter': presenter}

    pd_list = presenter.pdsession_set.filter(suspended=False, approved=True)

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

        context['pd_list'] = pd
        context['range'] = page_range

    return render(request, 'v3/final/presenter-landing.html', context)


def delete_comment(request):
    if request.POST and request.user.is_authenticated:
        comment_id = int(request.POST['comment_id'])
        comment = Comment.objects.get(pk=comment_id)
        presenter = comment.pd.presenters.all()[0]
        if request.user == comment.user.user or presenter.user == request.user:
            comment.delete()
    return HttpResponse('Success')


def comment(request):
    if request.POST and request.user.is_authenticated:
        pd_id = int(request.POST['pd_id'])
        reply_id = int(request.POST['reply_id'])
        parent_id = int(request.POST['reply_id'])
        print parent_id
        message = request.POST['msg']
        user = request.user.profile
        pd = PdSession.objects.get(pk=pd_id)
        user_owns = False
        for purchase in Purchase.objects.filter(user=user):
            if purchase.pdsession == pd:
                user_owns = True

        if message or not message.isspace() and user_owns:

            if pd.allow_email_notification_on_comment:
                presenter = pd.presenters.all()[0]
                msg = "Hello, " + presenter.user.first_name + ".\n\n"+ request.user.first_name +" "+ request.user.last_name+" posted the comment \n\'"+message+"\'\n" \
                                                        "\nOn your PD session titled '"+ pd.name +".' You can prevent further notifications such as this "\
                                                        "one by unclicking enable comments on notification when editing the current session in the" \
                                                        " session tab of the presenter hub.\n\nPD Squirrel admin team."
                subject = 'User Comment Notification'
                # Sets up email to be handled by task manager and is non blocking
                tasks.sendMail.apply_async([[presenter.user.email], subject, msg])

            if reply_id == 0:
                comment = Comment(message=message, user=user, pd=pd)
                comment.save()
                reply_id = comment.id
            else:
                parent = Comment.objects.get(pk=reply_id)
                comment = Comment(message=message, user=user, pd=pd, parent = parent)
                comment.save()

        reply = Comment.objects.get(pk=reply_id)
        context = {
                'comment': comment,
                'reply': reply
                }
        return render(request, 'v3/final/ajax/comment-reply.html', context)



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

# Error pages

def handler404(request):
    response = render_to_response('v3/final/error/404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler400(request):
    response = render_to_response('v3/final/error/400.html', {}, context_instance=RequestContext(request))
    response.status_code = 400
    return response

def handler403(request):
    response = render_to_response('v3/final/error/403.html', {}, context_instance=RequestContext(request))
    response.status_code = 403
    return response

def handler500(request):
    response = render_to_response('v3/final/error/500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response
