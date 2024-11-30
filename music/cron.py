from django_cron import CronJobBase, Schedule
from django.utils import timezone
from .models import Purchased, CustomerProfile

class UpdateSubscriptionStatusJob(CronJobBase):
    schedule = Schedule(run_every_mins=1440)  
    code = 'music.update_subscription_status'  

    def do(self):
        today = timezone.now().date() 
        purchased_items = Purchased.objects.filter(end_date__lt=today)
        for purchase in purchased_items:
            user_profile = purchase.user.customerprofile
            user_profile.is_subscribed = False
            user_profile.save()
        valid_purchases = Purchased.objects.filter(end_date__gte=today)
        for purchase in valid_purchases:
            user_profile = purchase.user.customerprofile
            user_profile.is_subscribed = True
            user_profile.save()
