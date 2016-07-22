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

'''
return card - either saved / new card

create a card
return card
'''


def payment_process(request):
    ''' Handles the ajax form on the detail.html page '''

    if request.POST:

        # Gather variables, retreive customer instance.
        pd_id = int(request.POST['pd_id'])
        pd = PdSession.objects.get(pk=pd_id)
        appuser = request.user.profile
        customer=stripe.Customer.retrieve(request.user.profile.stripe_id)


        # Return error message instead of confirmation form if they own the session.
        for x in Purchase.objects.filter(user=appuser):
            if pd == x.pdsession:
                return HttpResponse("pd owned.")

        # Initial purchase form post. If using a new card, token comes from stripe.
        # Otherwise, token is a saved source from a customer instance
        if 'new_card' in request.POST:
            token = stripe.Token.retrieve(request.POST['stripeToken'])
            context = {'token' : token, 'pd' : pd}
            return render(request, 'v3/final/purchase-confirmation.html', context)
        elif 'existing_card' in request.POST:
            source_id = request.POST['saved_card']
            source = None
            for s in customer.sources.data:
                if source_id == s.id:
                    source = s
            context = {'source' : source, 'pd' : pd }
            return render(request, 'v3/final/purchase-confirmation.html', context)


        # Second form post. token_id is the token generated from stripe if they are using
        # a new card, otherwise source_id is used from a saved card. A user has the option
        # to save the new card they input, by ticking the box.
        if 'confirm' in request.POST:
            if 'token_id' in request.POST:
                token = request.POST['token_id'] #token id

                # Save card for later use & charge customer. Token can only be used once,
                # so the card id is given instead. A customer id must also be passed when not
                # directly using a token.
                if 'save_card' in request.POST:
                    card = customer.sources.create(source=token)
                    stripe.Charge.create(amount=1000, customer=customer.id, currency='cad', source=card.id)
                    messages.add_message(request, messages.SUCCESS, 'Purchase successful, enjoy your session! Your card has been saved for future purchases. If you wish to remove it, you may do so on your account options page.')
                else:
                    # Continue with purchase, by using the token. No customer info is needed.
                    stripe.Charge.create(amount=1000, currency='cad', source=token)
                    messages.add_message(request, messages.SUCCESS, 'Purchase successful, enjoy your session!')

            # Customer is using a saved card
            elif 'source_id' in request.POST:
                source = request.POST['source_id']
                stripe.Charge.create(amount=1000, customer=customer.id, currency='cad', source=source)
                messages.add_message(request, messages.SUCCESS, 'Purchase successful, enjoy your session!')

            # Regardless of payment method, log a database entry of a purchase
            payment = Purchase(user=request.user.profile,pdsession=pd,price=pd.price,success=True)
            payment.save()


        # Using a credit does not need double confirmation, since no charge is made.
        if 'use_credit' in request.POST:
            if appuser.remaining_pd > 0:
                appuser.remaining_pd -= 1
                appuser.save()
                payment = Purchase(user=request.user.profile,pdsession=pd,price=0,success=True,credit_used=True)
                payment.save()
                messages.add_message(request, messages.SUCCESS, 'Purchase successful, enjoy your session!')
            else:
                messages.add_message(request, messages.ERROR, 'You do not have a sufficent number of credits.')

        return HttpResponseRedirect('/pd/' + str(pd.pk) + '/' )
