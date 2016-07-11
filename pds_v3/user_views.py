from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import string, hashlib, random
from django.contrib.auth import  hashers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from pds_v3.models import PdSession, AppUser, LawSociety, LawSocietyOverride, Purchase
from django.core.mail import send_mail
from django.contrib import messages
from .forms import CaptchaForm
from pds_v3.forms import PdSessionForm
import datetime
import tasks


import json, uuid, random, string, stripe, urllib, re

import stripe
stripe.api_key = "sk_test_Rxq0kWwzxNPQfOSCEsAjVd7e"


from django.contrib.auth import authenticate, login, logout


def login_landing(request):
    return render(request, 'v3/final/login-new.html')

def activate(request, link_id):
    try:
        profile = AppUser.objects.get(activation_key=link_id)
        if profile.user.is_active:
            messages.success(request, 'This account is already activated, login below.')
        else:
            profile.user.is_active = True
            profile.user.save()
            messages.success(request, 'Account activation successful. Sign in below using your email address. Thanks for choosing us, and welcome to PD Squirrel.<br><br>We have credited your account with one free member credit that may be used for any PD Session of your choice.')
    except:
        messages.error(request, 'Account not found. Please check the link for errors.')

    return render(request, 'v3/final/login-new.html')

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
            if 'type' in request.POST:
                messages.success(request, 'Login Successful')
                return HttpResponseRedirect('/browse/')
            else:
                return HttpResponse("success")

        else:
            return HttpResponse("user not active")
    else:
        if 'type' in request.POST:
            messages.error(request, 'Incorrect login credentials')
            return render(request, 'v3/final/login-new.html')
        else:
            return HttpResponse("incorrect sign-in credentials")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")



def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def recover(request):
    if request.POST:
        email = request.POST["email"]
        try:
            user = User.objects.get(username = email)
        except:
            messages.warning(request, 'That email is not associated with an account, please try again.')
            return render(request, 'v3/final/recover.html')

        plainpass = randomword(10)
        password = hashers.make_password(plainpass)
        user.password = password
        user.save()
        msg = "Hello, " + user.first_name + ".\n\nWe have reset your password for you. Your new password for temporary use is:\n" + plainpass + \
                                                "\n\nPlease sign in and change it (in your My Account page).\n\nThank you,\n\nPD Squirrel admin team."
        send_mail('PD Squirrel Recovery', msg, 'noreply@pdsquirrel.ca', [user.email,'demondsoftware@gmail.com'], fail_silently=False)

        messages.success(request, 'You have been sent a recovery password to your email')
        return render(request, 'v3/final/login-new.html')

    else:
        return render(request, 'v3/final/recover.html')



def clean_join(data):
    username = data.POST["username"]
    password = data.POST["password"]
    return True



def join_success(request):
    return True

def update(request):
    type = request.POST["type"]
    if type == 'email':
        try:
            email = request.POST["email"]
            request.user.email = email
            request.user.save()
        except:
            return HttpResponse("error updating email")




def join(request):
    context = {'societies' : LawSociety.objects.all(), 'form' : CaptchaForm(), 'msg' : []}

    if request.POST:

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        terms = request.POST.get("terms", None)

        email = request.POST["email"]
        vemail = request.POST['vemail']
        password = request.POST["password"]
        vpassword = request.POST['password_verify']

        society = request.POST.get("society", 0)
        if not society:
            society=0
        else:
            society = int(society)

        if LawSociety.objects.filter(pk=society).exists():
            return_society = LawSociety.objects.get(pk=society)
            law_society_exists = True
        else:
            return_society = ""
            law_society_exists = False

        context = {
            'first_name' : first_name,
            'last_name' : last_name,
            'terms' : terms,
            'email' : email,
            'society': return_society
        }

        context["societies"] = LawSociety.objects.all()
        context["form"] = CaptchaForm()
        context["msg"] = []
        msg = []
        f = CaptchaForm(request.POST)

        if terms == None:
            context['msg'].append({'type' :'danger', 'body' : 'Please check the terms and conditions.'})

        elif not society:
            context['msg'].append({'type' :'danger', 'body' : 'The Society you selected is not a valid Society.'})

        elif not law_society_exists:
            context['msg'].append({'type' :'danger', 'body' : 'The Society you selected is not a valid Society.'})

        elif last_name.isspace() or not last_name:
            context['msg'].append({'type' :'danger', 'body' : 'Please enter a last name.'})

        elif first_name.isspace() or not first_name:
            context['msg'].append({'type' :'danger', 'body' : 'Please enter a first name.'})

        elif not f.is_valid():
            context['msg'].append({'type' :'danger', 'body' : 'Incorrect captcha information.'})

        elif User.objects.filter(username=request.POST['email']).exists():
            context['msg'].append({'type' :'danger', 'body' : "A user with that email address is already registered."})

        elif not email:
            context['msg'].append({'type' :'danger', 'body' :  'Please enter an email'})

        elif re.match('^\S*@\S*\.\S*', email) is None:
            context['msg'].append({'type' :'danger', 'body' : "Your email format is invalid."})

        elif email != vemail:
            context['msg'].append({'type' :'danger', 'body' : "Your email does not match."})

        elif password != vpassword:
            context['msg'].append({'type' :'danger', 'body' : "Your password does not match."})

        elif len(password)<8:
            context['msg'].append({'type' :'danger', 'body' :  'Please enter a password with a length of atleast 8 characters'})

        else:
            password = hashers.make_password(password)
            profile = AppUser.create(first_name=first_name,last_name=last_name, email=email,
                                  password=password,terms=terms, society=society)
            # Create activation key
            s = ''
            for i in range(12): s += string.lowercase[random.randint(0,25)]
            s += str(email)
            activation_key = hashlib.sha256(s).hexdigest()
            profile.activation_key = activation_key
            profile.save()
# Please click on the following link and use your email address to activate your membership account: https://pdsquirrel.ca/user/activate/%s\n\nThanks,\nThe PD Squirrel admin team" % (str(activation_key) + "/"
            msg = "Hello " + first_name + " " + last_name + ", and welcome to PD Squirrel!\n\n We are currently in a beta working with presenters at this time.\n"
            msg += " As soon as we are ready to go live, you will receive an account activation email from us.d"
            msg += " You can then just click on the link to activate your account.\n\nThanks,\nThe PD Squirrel admin team"
            subject = 'PD Squirrel Account Creation'
            send_to = [profile.user.email, 'demondsoftware@gmail.com', 'cdemond@cwdlaw.ca']

            tasks.sendMail.apply_async([send_to, subject, msg])

            context['msg'].append({'type' : 'success', 'body' : 'Thank you. We have sent a welcome email to you. You may close this page.'})
            logout(request)
            customer = stripe.Customer.create(email=email)
            profile.stripe_id = customer.id
            profile.save()
            return render(request, 'v3/final/join-success.html', context)

    return render(request, 'v3/final/join.html', context)


def dash(request):
    context = {}

    user_pd = Purchase.objects.filter(user=request.user.profile)
    user_pd_list = []
    for purchase_obj in user_pd:
        user_pd_list.append(purchase_obj.pdsession)

    if user_pd_list:
        paginator = Paginator(user_pd_list, 5)

        page = request.GET.get('page')
        try:
            pd = paginator.page(page)
        except PageNotAnInteger:
            pd = paginator.page(1)
        except EmptyPage:
            pd = paginator.page(paginator.num_pages)

        context['pd_list'] = pd

        if user_pd:
            page_range = range(1,pd.paginator.num_pages + 1)
        else:
            page_range = range(False)

        context['range'] = page_range



    return render(request, "v3/final/dash.html", context)

def reports(request):
    return render(request, 'v3/final/reports.html')


def presenter(request):
    pd = PdSession.objects.filter(presenters=request.user)
    return render(request, 'v3/presenter.html', {'pd': pd})


def presenter_edit_pd(request):
    try:
        pd_id = request.GET.get('pd_id', None)
        pd = PdSession.objects.get(pk=pd_id)
    except:
        return HttpResponse("error getting pd object")
    form = PdSessionForm(instance=pd)
    return render(request, 'v3/presenter-edit-pd.html', {'form' : form})

def become_presenter(request):
    return render(request, 'v3/final/become-presenter.html')


def add_user_ajax(request):
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    user = AppUser(user=User.objects.create_user(username, email, password))
    user.save()


def suspend_user(request,user_id):
    user = AppUser.objects.get(pk=user_id)
    user.active = 0
    return True

def activate_user(request, user_id):
    user = AppUser.objects.get(pk=user_id)
    user.active = 1
    return True

def auth_user(request):
    username = request.POST["username"]
    password = request.POST["password"]

    result = authenticate(username=username, password=password)
    if request is not None:
        if result.active:
            return HttpResponse("user is auth & active")
        else:
            return HttpResponse("user is auth & not active")
    else:
        return HttpResponse("request failed")


def change_email(request):
    old_email = request.user.email
    email = request.POST.get('email', False)
    email_confirm = request.POST.get('email_confirm', False)

    if not email:
        return options(request, msg=[('danger', 'Please enter an email')])
    if email != email_confirm:
        return options(request, msg=[('danger', 'please enter a matching email')])
    if re.match('^\S*@\S*\.\S*', email) is None:
        return options(request, msg=[('danger', 'Your email must be in a valid email form. Example: test@pdsquirrel.ca')])

    request.user.email = email
    request.user.username = email
    request.user.save()

    msg = "This Email is no longer linked with PD Squirrel. The username of your account has been changed too: " + str(email) + "\n Please" \
                                                                " do not reply to this message."


    send_mail('PD Squirrel account email change', msg, 'noreply@pdsquirrel.ca', [old_email], fail_silently=False)
    send_mail('PD Squirrel account email change', msg, 'noreply@pdsquirrel.ca', ['demondsoftware@gmail.com'], fail_silently=False)
    send_mail('PD Squirrel account email change', msg, 'noreply@pdsquirrel.ca', ['cdemond@cwdlaw.ca'], fail_silently=False)

    return options(request,msg=[('success','Email change successful')])


def change_membership(request):
    if request.POST:
        appuser = request.user.profile
        stripe_id = appuser.stripe_id

        #Retreive customer obj from stripe
        try:
            customer = stripe.Customer.retrieve(stripe_id)
        except:
            messages.add_message(request, messages.ERROR,
                    'Error retreiving your customer profile. No changes have been made')

        # If they are premium currently, they must be downgrading
        if appuser.is_premium == True:
            appuser.is_premium = False
            for sub in customer.subscriptions:
                sub.delete()


            # Revoke the monthly desposit
            task_id = appuser.increment_task_id
            result = tasks.incrementCredits.AsyncResult(task_id)
            result.revoke()


            # Remove id from databse (task no longer exists)
            appuser.increment_task_id = None
            appuser.save()

            messages.add_message(request, messages.SUCCESS, 'You are now a standard user. We hope to see you soon!')
        else:
            try:
                customer.default_source = request.POST['default_card']
                customer.save() #Save selected card
                customer.subscriptions.create(plan=117)
            except:
                messages.add_message(request, messages.ERROR, "There was an error while creating your subscription. Please make sure you have entered in a credit card")
                return HttpResponseRedirect('/user/options/')

            # After initial subscription creation, add credits
            request.user.profile.remaining_pd += 8

            # Wait a few seconds before setting up next deposit.
            tasks.rolloverSubscription.apply_async([request.user, 8], countdown=15)
            appuser.is_premium = True


            messages.add_message(request, messages.SUCCESS, "You are now a premium user. Thanks for choosing us!")


    appuser.save()
    return HttpResponseRedirect('/user/options/')





def change_pass(request):

    username = request.user.username
    password_old = request.POST.get('pass_old', False)
    double_check_password = request.POST.get('vpass', False)
    password = request.POST.get('password_new', False)
    auth_result =  authenticate(username=username, password=password_old)

    if auth_result is None:
        return options(request,msg=[('danger','Incorrect password. Authentication failed.')])

    if not password:
        return options(request, msg=[('danger', 'Please enter a new password')])

    if password != double_check_password:
        return options(request,msg=[('danger','New passwords must match.')])

    if len(password)<8:
        return options(request,msg=[('danger','Password must be over 8 characters long.')])


    password = hashers.make_password(password)
    request.user.password = password
    request.user.save()

    msg = "The password to your PD Squirrel account has been changed. If you did not authorize that, please contact our" \
          " support team."

    send_mail('PD Squirrel password change', msg, 'noreply@pdsquirrel.ca', [request.user.email,'demondsoftware@gmail.com'], fail_silently=False)
    send_mail('PD Squirrel password change', msg, 'noreply@pdsquirrel.ca', ['demondsoftware@gmail.com'], fail_silently=False)
    send_mail('PD Squirrel password change', msg, 'noreply@pdsquirrel.ca', ['cdemond@cwdlaw.ca'], fail_silently=False)

    messages.success(request, 'Password change successful, please sign in using your new password')
    return HttpResponseRedirect('/browse/')


def options(request, msg=False):
    society = request.user.profile.society.all()[0].name
    customer_id = request.user.profile.stripe_id
    customer = stripe.Customer.retrieve(customer_id)
    context = {'user' : request.user, 'society':society, 'msgs':msg, 'customer':customer}

    return render(request, "v3/final/account-options.html", context)

def purchase_report(request,):
    user = AppUser.objects.get(user=request.user)
    purchases = Purchase.objects.filter(user=user)
    total= 0.00
    tax_total = 0.00
    before_tax = 0
    for p in purchases:
        if p.credit_used == False:
            p.price = p.price / 1.15
            before_tax = before_tax + p.price
            p.tax = 0.15 * p.price
            tax_total= tax_total + p.tax
            p.total = p.tax + p.price
            total = total + p.total
    context = {'purchases': purchases, 'total': ("%.2f" % total), 'total_tax':("%.2f" % tax_total), 'before_tax':("%.2f" % before_tax)}
    return render(request, 'v3/final/reports/purchases.html', context)

def del_card(request):
    if request.POST:

        customer = stripe.Customer.retrieve(request.user.profile.stripe_id)
        card_id = request.POST['cardid']

        # if card used for subscription, user must downgrade first.
        if card_id == customer.default_source and request.user.profile.is_premium:
            messages.add_message(request, messages.ERROR, 'This card is linked to your monthly subscription. To remove it, select another card for monthly billing or downgrade to standard.')
            return HttpResponseRedirect('/user/options/')

        # Delete card
        for x in customer.sources.data:
            if x.id == card_id:
                try:
                    x.delete()
                    messages.add_message(request, messages.SUCCESS, 'Card removed')
                except:
                    messages.add_message(request, messages.SUCCESS, 'Card removal error')

    return HttpResponseRedirect('/user/options/')

def default_payment(request):
    ''' Updates customers default payment method for monthly billing '''
    if request.POST:
        try:
            card_id = request.POST['card_id']
            customer = stripe.Customer.retrieve(request.user.profile.stripe_id)
            customer.default_source = card_id
            customer.save()
            messages.add_message(request, messages.SUCCESS, 'Default payment method updated')
        except:
            messages.add_message(request, messages.ERROR, 'There was an error updating your default payment method.')
        finally:
            return HttpResponseRedirect('/user/options/')


def add_card(request):
    if request.POST:
        try:
            token = request.POST['stripeToken']
            customer = stripe.Customer.retrieve(request.user.profile.stripe_id)
            customer.sources.create(source=token)
            request.user.profile.has_card = True
            request.user.profile.save()
            return HttpResponseRedirect('/user/options/')

        except:
            return options(request, msg=[('danger','Error adding card')])
    else:
        return HttpResponseRedirect('/user/options/')
