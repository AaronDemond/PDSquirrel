from __future__ import absolute_import
from celery import shared_task
import stripe


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
                wait_period = datetime.utcnow() + timedelta(hours=2)
                rolloverSubscription().apply_async((user),eta=wait_period)


@shared_task
def rolloverSubscription(user):
    ''' Sets up the next celery task which adds credits.
        This task should be ran approx 1 day after most
        recent subscription end time, to give the charge time
        to go through.
    '''

    # If user has active plan
    user.profile.refresh_from_db()
    if customer.subscriptions.data:
        if customer.subscriptions.data[0].status == 'active':
            if customer.subscriptions.data[0].plan.id == '117':

                # Setup credit deposit for the cycle end date
                customer = stripe.Customer.retrieve(id=user.profile.stripe_id)
                end_time_stamp = customer.subscriptions.data[0].current_period_end
                end_time_obj = datetime.datetime.fromtimestamp(end_time_stamp)
                incrementCredits().apply_async((request.user, 8), eta=end_time_obj)


