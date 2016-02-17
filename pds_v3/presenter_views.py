from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
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
	return HttpResponse('Unable to parse date')

    #add day to make end inclusive
    end = end + datetime.timedelta(days=1)


    #tally takes and earnings
    ppd = request.user.presenter.pdsession_set.filter(approved=True)
    opening_balance = 0 
    total_earnings = 0
    for pd in ppd:
	pd.takes = pd.purchase_set.filter(date__range=[start,end]).count()

	#calculate earnings within date range
	pd.earnings = sum([purchase.price * 0.6 for purchase in pd.purchase_set.filter(date__range=[start,end]) if not purchase.credit_used])
	pd.earnings += sum([2 for purchase in pd.purchase_set.filter(date__range=[start,end]) if purchase.credit_used])
	total_earnings += pd.earnings

	#calculate earnings prior to date range
	pd.prior = sum([purchase.price * 0.6 for purchase in pd.purchase_set.filter(date__lt=start) if not purchase.credit_used])
	pd.prior += sum([2 for purchase in pd.purchase_set.filter(date__lt=start) if purchase.credit_used])
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

        context['start'] = datetime.datetime(year=2015, month=01, day=01)

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
	non_pending_count = len([x for x in ppd if x.approved])
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

                #datedict with 'year' 'mont' 'date'
                start_dict = dfi(request.POST['start'], True)
                end_dict = dfi(request.POST['end'], True)

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
		presenter.credentials = request.POST['credentials']
		presenter.bio = request.POST['bio']
		if request.FILES:
		    presenter.image = request.FILES['photo']
		presenter.save()
		messages.add_message(request, messages.SUCCESS,
			'Account successfully updated.')
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=info')

	    if 'edit-pres-private' in request.POST:
		presenter.phone = request.POST['number']
		presenter.law_firm = request.POST['law_firm']
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

            #request pd be suspended
            if 'suspend-request' in request.POST:
                pd = PdSession.objects.get(pk=request.POST['session_id'])
                if pd.presenter_approved == False:
                    pd.delete()
                    messages.add_message(request, messages.SUCCESS, 'Session Removed')
                else:

                    messages.add_message(request, messages.INFO, 'Thank you for your input. \
                            we will review your removal request.')
                    pd.suspend_request = True
                    pd.suspend_reason = request.POST['reason']
                    pd.save()

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
		if pd.edited:
		    pd.name = pd.edits.latest().name
		    messages.add_message(request, messages.SUCCESS, 'Thank you for releasing \
                        your edited PD Session titled \'%s\'. When accepted by us, it will be listed on the Site, and offered by us to all PD Squirrel members.' % pd)
		else:
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

		    return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')


		#check file type 



                pd_description = request.POST['description']
                subjects = request.POST.getlist('subject') 
                pdaud = request.POST['recording']  #Recorded using recorder

                if pdaud is not None:
                    pdaud = PdAudio.objects.get(pk=int(pdaud))
		    pdaud.used = True
		    pdaud.save();
                    new_session = PdSession(name=pd_name,description=pd_description, pdaudio=pdaud, approved=False)
                else:
                    if not request.FILES['audio_file'].name.lower().endswith(('.wav', '.mp3')):
                        messages.add_message(request, messages.ERROR, 'Please upload the correct file type')
                        return HttpResponseRedirect('/user/presenter/dash/?direct_to=upload')

                    new_session = PdSession(name=pd_name,description=pd_description, audio_file=request.FILES['audio_file'], approved=False)

                    #get length if it is mp3.. need to convert wav
                    if request.FILES['audio_file'].name.lower().endswith(('.mp3')):
                        song = MP3(new_session.audio_file.name)
                        seconds = song.info.length
                        m, s = divmod(seconds, 60)
                        h, m = divmod(m, 60)
                        new_session.duration = "%02d:%02d" % (m, s)
                        new_session.save()
                    else:
                        subprocess.call(('lame --preset insane %s' % new_session.audio_file.name), shell=True)
                        new_path = new_session.audio_file.name[:-3] + 'mp3'
                        new_session.audio_file = new_path
                        new_session.save()

                new_session.save()
                for sub_id in subjects:
                    subject = Subject.objects.get(pk=sub_id)
                    new_session.subject.add(subject)
                counter = 0
                for afile in request.FILES:
                    if counter > 0:
                        attachment = PdAttachment(attachment=request.FILES[afile])
                        attachment.save()
                        new_session.attachments.add(attachment)
                    counter+=1

                new_session.presenters.add(Presenter.objects.get(user=request.user))
		
		

		messages.add_message(request, messages.INFO, "Thank you for uploading your PD Session, titled '%s'. \
			Click below to preview and release." % new_session)

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

            #change must be approved
            pd.presenter_approved = False
            pd.edited = True

            #gather post data
            name = request.POST['name']
            description = request.POST['description']
            subjects = request.POST.getlist('subjects')
            if 'audio_file' in request.FILES:
                audio_file = request.FILES['audio_file']
            else:
                audio_file = False


            #bounce if terms are not accepted
            if 'p-terms' not in request.POST:
                messages.add_message(request, messages.ERROR, 'You must accept the \
                        Terms and Conditions before editing content.')
                context['sesh'] = pd(name=name, description=description)
                return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')

            #create the edit
            edit = PdSessionEdit(name=name, description=description)
            if audio_file:
                edit.audio_file = audio_file
            #save before adding subjects to avoid foreignkey error (edit does not exist yet)
            edit.save()
            for subject_id in subjects:
                subject = Subject.objects.get(pk=subject_id)
                edit.subjects.add(subject)
            edit.save()
            pd.edits.add(edit)
            pd.save()
            messages.success(request,'Edit successful. If you are happy with your session, click \'Release Session\'.')


        return HttpResponseRedirect('/user/presenter/dash/?direct_to=sessions')

    else:
	if pd.edited:
	    edit = pd.edits.latest('date')
            context['sesh'] = fuseEdit(edit,pd)
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

	audio_to_hide = PdAudio.objects.filter(name=name, appuser=au)
	for a in audio_to_hide:
	    a.hidden = True;
	    a.save()

	pda = PdAudio(name=name, audio=upload, appuser=au)

	pda.save()
	pda.convertToMp3()
	pda.mp3_location = pda.getMp3Location();
	data_test = serializers.serialize("json", [pda]);
	return HttpResponse(data_test);
	#return HttpResponse("Saved Succesfully")


	#subprocess.call(('lame --preset insane %s' % filename), shell=True)

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











