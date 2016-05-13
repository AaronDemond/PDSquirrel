from pds_v3.models import PdSession, AppUser, LawSocietyOverride, Purchase, MembershipPaymentRecord, MembershipCancellationRecord
import json
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

'''
return card - either saved / new card

create a card
return card
'''


def payment_process(request):
    if request.POST:
     
        pd_id = int(request.POST['pd_id'])
        pd = PdSession.objects.get(pk=pd_id)
        appuser = request.user.profile


        for x in Purchase.objects.filter(user=request.user.profile):
            if pd == x:
                return HttpResponse("pd owned.")

        # Using new card
        if 'new_card' in request.POST:
            token = stripe.Token.retrieve(request.POST['stripeToken'])
            context = {'token' : token, 'pd' : pd}
            return render(request, 'v3/final/purchase-confirmation.html', context)

        if 'confirm' in request.POST:
            token = request.POST['token'] #token id

            #Save card for later use
            if 'save_card' in request.POST:
                customer=stripe.Customer.retrieve(request.user.profile.stripe_id)
                card = customer.sources.create(source=token)
                stripe.Charge.create(amount=1000, customer=customer.id, currency='cad', source=card.id)
                messages.add_message(request, messages.SUCCESS, 'Purchase successful, enjoy your session! Your card has been saved for future purchases. If you wish to remove it, you may do so on your account options page.')
            else:
                #Continue with purchase
                messages.add_message(request, messages.SUCCESS, 'Purchase successful, enjoy your session!')
                stripe.Charge.create(amount=1000, currency='cad', source=token)

            payment = Purchase(user=request.user.profile,pdsession=pd,price=pd.price,success=True)
            payment.save()

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
                #return HttpResponse("Card declined.")

        messages.add_message(request, messages.SUCCESS, 'Purchase successful, enjoy your session!')
        #return HttpResponseRedirect('/pd/' + str(pd.pk) + '/' )

