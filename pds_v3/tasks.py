from __future__ import absolute_import
from celery import shared_task
import stripe, datetime
from django.core.mail import send_mail

@shared_task
def sendMail(send_to, subject, msg):
    send_mail(subject, msg, 'admin@pdsquirrel.ca', [send_to], fail_silently=False)
    

@shared_task
def incrementCredits(user, amount):
    ''' Checks User obj has an active plan, if so, adds credits.
        The initial time is given when a new subscription is created,
        afterwhich rollover is called each time to gather the new
        deposit time.
    '''

    # If user has active plan
    user.profile.refresh_from_db()
    customer = stripe.Customer.retrieve(id=user.profile.stripe_id)
    if customer.subscriptions.data:
        if customer.subscriptions.data[0].status == 'active':
            if customer.subscriptions.data[0].plan.id == '117':

                # Plan active, add credits
                user.profile.remaining_pd += amount
                user.profile.save()

                # Allow time for new charge to go through,
                # at which point rollover gathers the new end date
                # and sets up another deposit for that time
                wait_period = datetime.datetime.now() + datetime.timedelta(hours=2)
                rolloverSubscription.apply_async((user, amount),eta=wait_period)


@shared_task
def rolloverSubscription(user, amount):
    ''' Sets up the next celery task which adds credits.
        This task should be ran after most
        recent subscription end time, to give the charge time
        to go through.
    '''

    # If user has active plan
    user.profile.refresh_from_db()
    customer = stripe.Customer.retrieve(id=user.profile.stripe_id)
    if customer.subscriptions.data:
        if customer.subscriptions.data[0].status == 'active':
            if customer.subscriptions.data[0].plan.id == '117':

                # Setup credit deposit for the cycle end date
                customer = stripe.Customer.retrieve(id=user.profile.stripe_id)
                end_time_stamp = customer.subscriptions.data[0].current_period_end
                end_time_obj = datetime.datetime.fromtimestamp(end_time_stamp)


                # This may be a bug with celery? Without this line the times
                # object is correct but the task instance incorrectly subtracts
                # 3 hours for its eta. Look into this.
                end_time_obj = end_time_obj + datetime.timedelta(hours=3)

                # Add task id to user
                #print 'Scheduled credit deposit for: ' + user.username
                t = incrementCredits.apply_async((user, amount), eta=end_time_obj)
                user.profile.increment_task_id = t.id
                user.profile.save()
