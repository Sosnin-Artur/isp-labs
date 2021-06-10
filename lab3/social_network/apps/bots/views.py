from django.shortcuts import render
import requests

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger(__name__)

def create_post(request):
    logger.info('start create post')
    user = User.objects.get(username = 'bot')
    token = 'f88de38bf88de38b620dc9725559b497361de40'
    version = 5.103
    domain = 'tproger'

    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                            'access_token': token,
                            'v': version,
                            'domain': domain,
                            'count': 5
                            }
                        )
    data = response.json()['response']['items']
    for news in data:
        try:
            if news['attachments'][0]['type']:
                img_url = news['attachments'][0]['photo']['sizes'][-1]['url']
            else:
                img_url = ''
        except:
            img_url = ''

        try:
            news['attachments'][0]['video']
        except:
            if news['text'] != '':
                in_post = Post.objects.filter(post_text = news['text'])
            else:
                in_post = Post.objects.filter(post_image_url = img_url)

            if not in_post:
                post = Post(author = user, post_text=news['text'], post_time = timezone.now(), post_image_url=img_url)
                post.save()
    logger.info('end create post')
    return HttpResponse('Complete ')
