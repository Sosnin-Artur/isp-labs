from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
from datetime import datetime, timedelta


import logging, asyncio
logger = logging.getLogger(__name__)

class Profile(models.Model):
    GENDER_CHOICE = (
        ("M", "M"),
        ("F", "F"),
        (None, "-"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('avatar', blank=True, upload_to = 'images/avatar/')
    gender =  models.CharField('gender', max_length=1,
                  choices=GENDER_CHOICE,
                  blank=True)
    city = models.CharField('city', max_length=100, blank=True)    

    birth_date = models.DateField('birthday', null=True, blank=True)
    
    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        logger.info('cteate user')
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    logger.info('save user')
    instance.profile.save()


class Status(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    online = models.DateTimeField('was online', null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_online_status(self):

        logger.info('get online status')
        status = ''
        timezone_delta = timedelta(hours=3, minutes=0)
        online_status_true = timedelta(minutes=5)
        user_online = self.online + timezone_delta

        if self.user.profile.gender == 'F':
            if user_online.date() == (datetime.now() - timedelta(days=1)).date():
                status = 'was online ' + user_online.time().strftime("%H:%M")
            elif timezone.now() - self.online < online_status_true:
                status = 'online'
            elif user_online.date() == datetime.now().date():
                status = 'was online ' + user_online.time().strftime("%H:%M")
            elif user_online.date().year == datetime.now().date().year:
                status = 'was online' + user_online.date().strftime("%d.%m") + ' in ' + user_online.time().strftime("%H:%M")
            else:
                status = 'was online ' + user_online.date().strftime("%d.%m.%Y") + ' in ' + user_online.time().strftime("%H:%M")
        else:
            if user_online.date() == (datetime.now() - timedelta(days=1)).date():
                status = 'was online ' + user_online.time().strftime("%H:%M")
            elif timezone.now() - self.online < online_status_true:
                status = 'was online'
            elif user_online.date() == datetime.now().date():
                status = 'was online' + user_online.time().strftime("%H:%M")
            elif user_online.date().year == datetime.now().date().year:
                status = 'was online' + user_online.date().strftime("%d.%m") + ' in ' + user_online.time().strftime("%H:%M")
            else:
                status = 'was online' + user_online.date().strftime("%d.%m.%Y") + ' in ' + user_online.time().strftime("%H:%M")
        return status

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    users_friend = models.ForeignKey(User, related_name = 'users_friend', on_delete = models.CASCADE)
    confirmed = models.BooleanField('assept', default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    follower_for = models.ForeignKey(User, related_name = 'follower_for', on_delete = models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'follower'
        verbose_name_plural = 'followers'
