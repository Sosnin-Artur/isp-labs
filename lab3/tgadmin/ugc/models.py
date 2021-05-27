from django.db import models

class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='id of user',
        unique=True,
    )
    
    name = models.TextField(
        verbose_name = "username",
    )       

    location = models.TextField(
        verbose_name = "username",
    )       

    bio = models.TextField(
        verbose_name = "bio",
    )

    def __str__(self):
        return f'(selfexterna_id) {self.name}'
    
    class Meta:
        verbose_name = "profile"

class Message(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Text',
    )
    created_at = models.DateTimeField(
        verbose_name='Time getting',
        auto_now_add=True
    )

    def __str__(self):
        return f'message {self.pk} or {self.profile}'
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Message'