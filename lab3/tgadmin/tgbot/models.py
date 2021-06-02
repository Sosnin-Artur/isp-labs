import requests

from django.db import models
from tgbot import utils


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)        
    deep_link = models.CharField(max_length=64, null=True, blank=True)
    
    is_banned = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)        
    
    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def create_user(cls, update, context):
        data = utils.extract_user_data_from_update(update)
        u, created = cls.objects.create(user_id=data["user_id"], defaults=data)

        if created:
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip(): 
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user_and_created(cls, update, context):
        """ python-telegram-bot's Update, Context --> User instance """
        data = utils.extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)

        if created:
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip(): 
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update, context):
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, string):
        """ Search user in DB, return User or None if not found """
        username = str(string).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @classmethod
    def delete_user_by_username_or_user_id(cls, string):
        """ Search user in DB, return User or None if not found """
        username = str(string).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).delete()        
        return cls.objects.filter(username__iexact=username).delete()

    def invited_users(self):  # --> User queryset 
        return User.objects.filter(deep_link=str(self.user_id), created_at__gt=self.created_at)

class Location(models.Model):
    users = models.ManyToManyField(User)
    country = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"user: {self.user}, created at {self.created_at.strftime('(%H:%M, %d %B %Y)')}"

    def save(self, *args, **kwargs):
        super(Location, self).save(*args, **kwargs)                

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='profile')        
    country = models.CharField(max_length=20, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    @classmethod
    def create_profile(sender, **kwargs):
        if kwargs.get('created', False):
            Profile.objects.create(user=kwargs['instance'])


