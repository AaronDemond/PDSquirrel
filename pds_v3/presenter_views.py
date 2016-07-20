from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.core.mail import send_mail
from django.core import serializers
from django.core.files import File
import os
import subprocess
from django.core.files.base import File as DjangoFile
from django.views.decorators.csrf import csrf_exempt
from pds_v3.my_functions import date_from_input as dfi
from django.contrib import messages
from pds_v3.models import PdSession,Presenter, AppUser, LawSociety, \
LawSocietyOverride, Purchase, Subject, PdSessionEdit, PdAttachment, PdAudio
from pds_v3.views import fuseEdit

from django.core.exceptions import ObjectDoesNotExist
from mutagen.mp3 import MP3
import datetime


from django.forms.models import modelform_factory
from forms import PdSessionForm


def presenter_uploads(request):
    subjects = Subject.objects.all()
    recordings = PdAudio.objects.filter(appuser = request.user.profile, used = False, hidden = False)
    context = {'subjects' : subjects, 'recordings' : recordings}
    return render(request, 'v3/final/presenter-pages/final/upload.html', context)

def getEditModel(request, id):
    pd = PdSession.objects.get(pk=id)
    context = {'sesh' : pd}

    return render(request,'v3/final/presenter-pages/model-edit.html', context)


def handle_uploaded_file(f):
    destination = open('')


def analytics_report(request):

    start = request.POST.get('start', False)
    end = request.POST.get('end', False)

    if not start or not end:
        start = request.GET.get('start', False)
        end = request.GET.get('end', False)

    if request.GET:
        report_type = 'pdf'
    else:
        report_type = 'html'



    #datetime objects for range comparison
    try:
        start = dfi(start)
        end = dfi(end)
        end = end + datetime.timedelta(days=1)
    except:
        context = {'type': None}
        return render_to_response('v3/final/presenter-pages/final/reports/analytics.html', context)





    #tally takes and earnings
    ppd = request.user.presenter.pdsession_set.filter(approved=True)
    opening_balance = 0
    total_earnings = 0
    for pd in ppd:
        pd.takes = pd.purchase_set.filter(date__range=[start,end], success=True).count()

        #calculate earnings within date range
        pd.earnings = sum([purchase.price * 0.6 for purchase in pd.purchase_set.filter(date__range=[start,end], success=True) if not purchase.credit_used])
        pd.earnings += sum([2 for purchase in pd.purchase_set.filter(date__range=[start,end], success=True) if purchase.credit_used])
        total_earnings += pd.earnings

        #calculate earnings prior to date range
        pd.prior = sum([purchase.price * 0.6 for purchase in pd.purchase_set.filter(date__lt=start, success=True) if not purchase.credit_used])
        pd.prior += sum([2 for purchase in pd.purchase_set.filter(date__lt=start, success=True) if purchase.credit_used])
        opening_balance += pd.prior

    #since there is no payout yet, closing is all earnings to date.
    closing_balance = total_earnings + opening_balance
    total_takes = sum([pd.takes for pd in ppd])

    #decrement time to original inorder display properly
    end = end - datetime.timedelta(days=1)
    user = request.user.profile
    context = {'ppd' : ppd, 'start': start, 'end': end, \
            'open' : opening_balance, 'close' : closing_balance, \
            'total_earnings': total_earnings, 'total_takes' : total_takes,
            'type': report_type, 'request' : request}

    #use render_to_response because render causes 500 error using request variable from ajax (not serialized?)
    return render_to_response('v3/final/presenter-pages/final/reports/analytics.html', context)


def dash(request, msg=False):

    if request.user.profile.is_presenter == True:
        uploadform = PdSessionForm()
        context = {'msg' : msg }

        presenter = Presenter.objects.filter(user=request.user)[0]
        context['presenter'] = presenter

        context['start'] = datetime.datetime(year=2016, month=01, day=01)

        context['end'] = datetime.datetime.now()
        context['total_earnings'] = 0
        context['total_takes'] = 0
        context['open'] = 0
        context['close'] = 0
        context['paid'] = 0
        #ppd = presenter PD
        context['ppd'] = request.user.presenter.pdsession_set.all()
        pending_count = 0
        takes_count = 0
        cumulative_earnings = 0.00
        for x in context['ppd']:
            if x.edited or not x.approved:
                pending_count += 1
            takes_count += x.total_takes
            cumulative_earnings += (x.total_sales * 0.67) + (x.total_credits * 2)


        ppd = request.user.presenter.pdsession_set.all()
        total_takes = sum([x.purchase_set.all().count() for x in ppd])
        pending_count = len([x for x in ppd if x.edited and not x.approved or not x.approved])
        edit_count = len([x for x in ppd if x.edited and x.approved])
        non_pending_count = len([x for x in ppd if x.approved and not x.suspended])
        context['listed_count'] = non_pending_count
        context['edit_count'] = edit_count
        context['takes_count'] = total_takes
        context['pending_count'] = pending_count
        context['cumulative_earnings'] = cumulative_earnings


        if presenter is not None:
            context['pd'] = PdSession.objects.filter(presenters=presenter).order_by('-upload_date', 'name')
            earnings = 0
        if request.POST:

            if 'date-rng' in request.POST:
                context['report_ran'] = 'True'

                #datetime objects for range comparison
                start = dfi(request.POST['start'])
                end = dfi(request.POST['end'])

                if start == False or end == False:
                    return HttpResponse('Please enter a correctly formatted date.')

                context['start'] = start
                context['end'] = end

                all_purchases = []
                presenter_pd = PdSession.objects.filter(presenters=presenter).order_by('-upload_date', 'name')

                #add one day to end so it is inclusive of the last day for tange search
                end = end + datetime.timedelta(days=1)

                for pd in presenter_pd:
                    purchases = Purchase.objects.filter(pdsession=pd, date__range=[start,end])
                    purchases_other = Purchase.objects.filter(pdsession=pd, date__range=[datetime.datetime(2015,01,01),start])
                    pd.takes = len(purchases)


                    pd.tmp_earnings = 0
                    for p in purchases_other:
                        if p.credit_used:
                            pd.tmp_earnings += 2.0
                        else:
                            pd.tmp_earnings += 2.0
                    context['open'] += pd.tmp_earnings

                    pd.tmp_earnings = 0
                    for p in purchases:
                        if p.credit_used:
                            pd.tmp_earnings += 2.0
                        else:
                            pd.tmp_earnings += 2.0
                    context['total_earnings'] += pd.tmp_earnings
                    context['total_takes'] += pd.takes


                context['close'] = context['open'] + context['total_earnings']

                context['pd_earnings'] = presenter_pd

                return render(request, 'v3/final/presenter-pages/final/dash.html', context)
                return HttpResponseRedirect('/user/presenter/dash/')


            if 'edit-pres-public' in request.POST:
                from django.core.files import File
                presenter.credentials = request.POST['credentials']
                presenter.law_firm = request.POST['law_firm']
                presenter.bio = request.POST['bio'].lstrip()
                presenter.public_email = request.POST['public_email']
                presenter.url = request.POST['url']
                if 'clear_photo' in request.POST:
                    presenter.image = None
                    presenter.placeholder_type = 1;
                if request.FILES:
                    presenter.image = request.FILES['photo']
                    presenter.placeholder_type = 2;

                presenter.save()
                messages.add_message(request, messages.SUCCESS,
                        'Presenter page successfully updated.')
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=info')

            if 'edit-pres-private' in request.POST:
                presenter.phone = request.POST['number']
                presenter.save()
                messages.add_message(request, messages.SUCCESS,
                    'Account successfully updated.')
                presenter.save()
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=private')


            #Cancel an edit
            if 'edit-c' in request.POST:
                edit = PdSessionEdit.objects.get(pk=request.POST['edit'])
                edit.delete()
                messages.add_message(request, messages.INFO, 'Your edit has been removed.')
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')

            # request removal of session
            # If it has purchases, unlist it (suspend) otherwise delete.
            if 'suspend-request' in request.POST:
                pd = PdSession.objects.get(pk=request.POST['session_id'])
                if pd.purchase_set.exists():
                    pd.suspended = True
                    pd.suspend_reason = request.POST['reason']
                    pd.save()
                    messages.add_message(request, messages.SUCCESS, 'Session Removed from listing. Users who have previously purchased this session will still have access, and you may still make changes.')
                else:
                    # Delete and make available the audio for re-upload
                    pd.delete()
                    messages.add_message(request, messages.SUCCESS, 'Session permanently deleted')
                    if bool(pd.pdaudio):
                        pd.pdaudio.used = False
                        pd.pdaudio.save()
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')

            if 'suspend-cancel' in request.POST:
                pd = PdSession.objects.get(pk=request.POST['session_id'])
                pd.suspend_request = False
                pd.save()
                messages.add_message(request, messages.SUCCESS, 'Your session is no longer pending removal.')
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')

            #approve PD session (ready for quality test by admins)
            if 'p-approved' in request.POST:
                pd = PdSession.objects.get(pk=request.POST['session_id'])
                messages.add_message(request, messages.SUCCESS, 'Thank you for releasing \
                    your PD Session titled \'%s\'. When accepted by us, it will be listed on the Site, and offered by us to all PD Squirrel members.' % pd)
                pd.presenter_approved = True
                pd.save()
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')



            if 'p-terms' not in request.POST:
                messages.add_message(request, messages.ERROR, 'You must accept the \
                        Terms and Conditions before uploading content.')

                return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')


            #New upload
            form = PdSessionForm(request.POST, request.FILES)
            if form.is_valid():
                if 'name' in request.POST:
                    pd_name = request.POST['name']

                else:
                    messages.add_message(request, messages.ERROR, 'Please provide a \
                                                title.')

                    return HttpResponseRedirect('/user/presenter/dash/?direct_to=upload')


                pd_description = request.POST['description']
                subjects = request.POST.getlist('subject')

                if 'allow_email_notification_on_comment' in request.POST:
                    allow_email_notification_on_comment = True
                else:
                    allow_email_notification_on_comment = False

                if 'disable_comments' in request.POST:
                    disable_comments = False
                else:
                    disable_comments = True

                if not subjects:
                    messages.add_message(request, messages.ERROR, 'Please select at least one subject')
                    return HttpResponseRedirect('/user/presenter/dash/?direct_to=upload')




                pdaud = request.POST.get('recording', False)
                if pdaud:
                    if int(pdaud) == 0:
                        messages.add_message(request, messages.ERROR, 'Please select a recording')
                        return HttpResponseRedirect('/user/presenter/dash/?direct_to=upload')

                    pdaud = PdAudio.objects.get(pk=int(pdaud))
                    pdaud.used = True
                    pdaud.save();
                    mp3_obj = MP3(pdaud.getMp3Location())
                    new_session = PdSession(name=pd_name,description=pd_description, pdaudio=pdaud, approved=False, presenter_approved=True, comments_disabled=disable_comments, allow_email_notification_on_comment = allow_email_notification_on_comment)
                    counter = 1 #file counter. 1 if pd audio, 0 if audio from client pc
                else:
                    audio_file = request.FILES.get('audio_file', False)

                    counter = 0
                    if audio_file == False:
                        messages.add_message(request, messages.ERROR, 'Please upload a file')
                        return HttpResponseRedirect('/user/presenter/dash/?direct_to=upload')

                    _name = audio_file.name.lower()

                    if not (_name.endswith('.mp3') or _name.endswith('.wav')):
                        messages.add_message(request, messages.ERROR, 'Please upload an MP3 or a WAV file')
                        return HttpResponseRedirect('/user/presenter/dash/?direct_to=upload')

                    new_session = PdSession(name=pd_name,description=pd_description, audio_file=audio_file, approved=False, presenter_approved=True, comments_disabled=disable_comments, allow_email_notification_on_comment = allow_email_notification_on_comment)
                    new_session.save()

                    # get an MP3 object (mutagen lib)
                    if audio_file.name.lower().endswith(('.mp3')):
                        mp3_obj = MP3(new_session.audio_file.name)
                    else:
                        subprocess.call(('lame --preset insane %s' % new_session.audio_file.name), shell=True)
                        new_path = new_session.audio_file.name[:-3] + 'mp3'
                        mp3_obj = MP3(new_path)
                        new_session.audio_file = new_path
                        new_session.save()

                # get the duration
                seconds = mp3_obj.info.length
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                new_session.duration = "%02d:%02d" % (m, s)
                new_session.save()

                for sub_id in subjects:
                    subject = Subject.objects.get(pk=sub_id)
                    new_session.subject.add(subject)
                for afile in request.FILES:
                    if counter > 0:
                        attachment = PdAttachment(attachment=request.FILES[afile])
                        attachment.save()
                        new_session.attachments.add(attachment)
                    counter+=1


                new_session.presenters.add(Presenter.objects.get(user=request.user))


                msg = request.user.username + ' has uploaded and released a new session'
                send_mail('new upload/release' , msg , 'support@pdsquirrel.ca', ['admin@pdsquirrel.ca', 'cdemond@pdsquirrel.ca'], fail_silently=False)

                messages.add_message(request, messages.INFO, "Thank you for uploading your PD Session, titled '%s'." % new_session)

                return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')
            else:
                return HttpResponseRedirect('/user/presenter/dash/')
        #get methods
        else:
            if 'direct_to' in request.GET:
                context['direct_to'] = request.GET['direct_to']

            if 'mysessions' in request.GET:
                return render(request, 'v3/final/presenter-pages/final/my-sessions.html', context)

            elif 'myaccount' in request.GET:
                context['presenter'] = presenter
                return render(request, 'v3/final/presenter-pages/final/account.html', context)

            elif 'landing' in request.GET:
                return render(request, 'v3/final/presenter-pages/final/landing.html', context)

            elif 'analytics' in request.GET:
                return render(request, 'v3/final/presenter-pages/final/analytics.html', context)
            elif 'testanalytics' in request.GET:
                return HttpResponse('test content');

            elif 'myinfo' in request.GET:
                return render(request, 'v3/final/presenter-pages/final/presenter-info.html', context)

            return render(request, 'v3/final/presenter-pages/final/dash.html', context)
    else:
        return HttpResponse("Authentication Error")



def edit(request, id):
    pd = PdSession.objects.get(pk=id)
    context = {'sesh' : pd, 'subjects' : Subject.objects.all()}
    if request.POST:


        #the following creates the edit
        if 'create-edit' in request.POST:

            #bounce if terms are not accepted
            if 'p-terms' not in request.POST:
                messages.add_message(request, messages.ERROR, 'You must accept the \
                        Terms and Conditions before editing content.')
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')

            #gather post data
            description = request.POST['description']
            name = request.POST.get('name', pd.name)
            subjects = request.POST.getlist('subjects')

            if 'allow_email_notification_on_comment' in request.POST:
                allow_email_notification_on_comment = True
            else:
                allow_email_notification_on_comment = False

            if 'disable_comments' in request.POST:
                disable_comments = False
            else:
                disable_comments = True

            if not subjects:
                messages.add_message(request, messages.ERROR, 'Please select a subject \
                        for you PD session.')
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')

            #create the edit
            edit = PdSessionEdit(name=name, description=description, comments_disabled = disable_comments, allow_email_notification_on_comment = allow_email_notification_on_comment)
            edit.save()

            # If there was a previous edit, use its data
            if pd.edited:
                old_edit = pd.edits.latest('date')
                edit.attachments = old_edit.attachments.all()

            edit.save()

            # Mark files to delete
            files_to_delete = request.POST.getlist('files_to_delete')
            for f in files_to_delete:
                attachment = PdAttachment.objects.get(pk=f)
                attachment.delete()



            # Add files & subjects to edit
            for afile in request.FILES:
                attachment = PdAttachment(attachment=request.FILES[afile])
                attachment.save()
                edit.attachments.add(attachment)
                pd.attachments.add(attachment)

            pd.subject.clear()
            for subject_id in subjects:
                subject = Subject.objects.get(pk=subject_id)
                pd.subject.add(subject)

            pd.edited = True
            edit.save()
            pd.edits.add(edit)


            # An edit now directly updates the model
            # Consider saving the original ..?
            #pd.subject = edit.subjects.all()
            pd.name = edit.name
            pd.description = edit.description
            pd.allow_email_notification_on_comment = edit.allow_email_notification_on_comment
            pd.comments_disabled = edit.comments_disabled
            pd.save()
            messages.success(request,'Edit successful.')

        return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')

    else:
        if pd.edited:
            edit = pd.edits.latest('date')
            pd.name=edit.name
            pd.description=edit.description

            context['session_subjects'] = edit.subjects.all()
            context['sesh'] = pd
            context['edit'] = edit
        else:
            context['session_subjects'] = pd.subject.all()

        return render(request, 'v3/final/presenter-pages/final/edit.html' , context)


def notice(request):
    pass



@csrf_exempt
def record(request):

    if 'del' in request.POST:
        aud_id = request.POST['aud_id']
        x = PdAudio.objects.filter(id=aud_id, appuser=request.user.profile)[0]
        x.hidden=True
        x.save();
        return HttpResponseRedirect('/record/');

    if 'upload' in request.POST:
        #wav binary
        au = request.user.profile
        upload = request.FILES['data']
        name = request.POST['name']
        pdaudio_id = request.POST.get('pdaudio_id', False)

        if pdaudio_id:
            audio_to_overwrite = PdAudio.objects.get(pk=pdaudio_id)
            audio_to_overwrite.audio = upload
            audio_to_overwrite.save()
            audio_to_overwrite.convertToMp3()
            resp = serializers.serialize("json", [audio_to_overwrite]);
        else:
            pda = PdAudio(name=name, audio=upload, appuser=au)
            pda.save()
            pda.convertToMp3()
            resp = serializers.serialize("json", [pda]);

        return HttpResponse(resp);

    else:

        audio = PdAudio.objects.filter(appuser = request.user.profile, used = False, hidden = False)
        c = {'audio_recordings': audio}


        return render(request, 'v3/final/presenter-pages/final/record.html', c)

def editRecording(request, r_id=False):
    pdaudio = PdAudio.objects.get(pk=r_id)
    fname = pdaudio.getMp3Location()
    f = open(fname, "rb")
    lol = list(f)
    c = {'pdaudio': pdaudio, 'f': f, 'lol': lol}
    return render(request, 'v3/final/presenter-pages/final/edit-recording.html', c)
