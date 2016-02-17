from pds_v3.models import PdSession, AppUser, LawSocietyOverride, Purchase, MembershipPaymentRecord, MembershipCancellationRecord
import datetime
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
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

	if appuser.remaining_pd > 0:
		appuser.remaining_pd -= 1

		price = pd.price
		payment = Purchase(user=request.user.profile,pdsession=pd,price=0,success=True,credit_used=True)
		payment.save()
		appuser.save()
	else:

		#currently a test api key
		stripe.api_key = "sk_test_Rxq0kWwzxNPQfOSCEsAjVd7e"
		token = request.POST['stripeToken']


		try:
		    charge = stripe.Charge.create(
			amount=1999,
			currency="cad",
			source=token,
			description="example charge"
		    )
		except stripe.CardError:
		    payment = Purchase(user=request.user,pdsession=pd,price=pd.price,success=False)
		    payment.save()
		    return HttpResponse("Card declined.")

		price = pd.price
		payment = Purchase(user=request.user.profile,pdsession=pd,price=price,success=True)
		payment.save()
	context = {'msg' : 'Thank you for your purchase. Enjoy this session.'}
	context['msgType'] = "success"
	context['own'] = 1
	context['pd'] = pd

        return render(request, 'v3/final/detail.html', context)
    else:
        return HttpResponse("Error")
