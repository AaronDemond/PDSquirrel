from pds_v3.models import PdSession, AppUser, LawSocietyOverride, Purchase, MembershipPaymentRecord, MembershipCancellationRecord
import datetime
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from simplemathcaptcha.fields import MathCaptchaField
__author__ = 'Aaron'
import stripe

def change_membership(request):
    if request.POST:
        membership_type = request.POST['type']
        appuser = request.user.profile
        if membership_type == '0':
            appuser.is_premium = False
        elif membership_type == '1':
            appuser.is_premium = True
            appuser.date_premium = datetime.datetime.now()

        appuser.save()
        return HttpResponse('success')
    else:
        return HttpResponse('Invlid request')




def payment_process(request):
    if request.POST:
     
        pd_id = int(request.POST['pd_id'])
        pd = PdSession.objects.get(pk=pd_id)
        appuser = request.user.profile


        for x in Purchase.objects.filter(user=request.user.profile):
            if pd == x:
                return HttpResponse("pd owned.")

        if 's_card' in request.POST:
            try:
                customer=stripe.Customer.retrieve(request.user.profile.stripe_id)
                stripe.Charge.create(amount=1000, currency='cad', customer=customer)
                messages.add_message(request, messages.SUCCESS, 'Purchase successful, enjoy your session!')
                payment = Purchase(user=request.user.profile,pdsession=pd,price=pd.price,success=True)
                payment.save()
            except:
                payment = Purchase(user=request.user,pdsession=pd,price=pd.price,success=False)
                payment.save()
                return HttpResponse("Card declined.")

            return HttpResponseRedirect('/pd/' + str(pd.pk) + '/' )


        if appuser.remaining_pd > 0:
            appuser.remaining_pd -= 1
            appuser.save()
            payment = Purchase(user=request.user.profile,pdsession=pd,price=0,success=True,credit_used=True)
            payment.save()

        else:
            stripe.api_key = "sk_test_Rxq0kWwzxNPQfOSCEsAjVd7e" #test key
            token = request.POST['stripeToken']

            try:
                charge = stripe.Charge.create(
                    amount=1999,
                    currency="cad",
                    source=token,
                    description="example charge"
                )
                payment = Purchase(user=request.user.profile,pdsession=pd,price=pd.price,success=True)
                payment.save()
            except stripe.CardError:
                payment = Purchase(user=request.user,pdsession=pd,price=pd.price,success=False)
                payment.save()
                return HttpResponse("Card declined.")

        messages.add_message(request, messages.SUCCESS, 'Purchase successful, enjoy your session!')
        return HttpResponseRedirect('/pd/' + str(pd.pk) + '/' )

    else:
        return HttpResponse("Error")
