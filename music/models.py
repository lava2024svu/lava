from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.models.signals import post_save

class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='artist_images/')

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cat_images/')

    def __str__(self):
        return self.name
    
    @receiver(post_migrate)
    def create_default_values(sender, **kwargs):
        default_values = [
            'Classical',
            'Hip Hop',
            'Traditional',
            'Rock',
            'Pop',
            'Syrian',
            'Foriegn',
            'Slow',
            'Song',
        ]

        for value_name in default_values:
            Category.objects.get_or_create(name=value_name)

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='album_covers/',blank=True,null=True,)
    views = models.PositiveIntegerField(default=0,blank=True,null=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Track(models.Model):
    title = models.CharField(max_length=100)
    textm = models.CharField(max_length=2000)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    duration = models.DurationField()
    audio_file = models.FileField(upload_to='audio_files/')
    views = models.PositiveIntegerField(default=0,blank=True,null=True)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Purchased(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            purchase_date = self.purchase_date.date()
            next_month = purchase_date.month + 1 if purchase_date.month < 12 else 1
            next_year = purchase_date.year if purchase_date.month < 12 else purchase_date.year + 1

            last_day_of_next_month = (purchase_date.replace(month=next_month, year=next_year, day=1) + timedelta(days=-1)).day
            new_day = min(purchase_date.day, last_day_of_next_month)

            self.end_date = purchase_date.replace(year=next_year, month=next_month, day=new_day)

        super().save(*args, **kwargs)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username} - {'Subscribed' if self.is_subscribed else 'Not Subscribed'}"
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)