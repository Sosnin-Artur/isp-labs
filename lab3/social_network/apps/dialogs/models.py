from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    reciever = models.ForeignKey(User, related_name = 'to_reciever', on_delete = models.DO_NOTHING)
    message_text = models.TextField('text message')
    message_image = models.ImageField('image', blank = True, upload_to = 'images/messages/')
    message_time = models.DateTimeField('time of sending')
    is_readed = models.BooleanField('readed', default=False)
    sender_visibility = models.BooleanField('sender visible', default=True)
    reciever_visibility = models.BooleanField('reviever visible', default=True)

    def __str__(self):
        return str(self.sender) + ' to ' + str(self.reciever)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'message'
