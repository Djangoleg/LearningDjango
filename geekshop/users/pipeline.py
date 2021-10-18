from urllib import request
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from geekshop.settings import MEDIA_USERS_IMAGE_PATH
from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200', 'personal')),
                                                access_token=response['access_token'],
                                                v='5.131')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        if data['sex'] == 1:
            user.userprofile.gender = UserProfile.FEMALE
        elif data['sex'] == 2:
            user.userprofile.gender = UserProfile.MALE

    if data['about']:
        user.userprofile.about = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year

        user.age = age

        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['personal']:
        if data['personal']['langs']:
            user.userprofile.languages = '|'.join(str(lang) for lang in data['personal']['langs'])

    if data['photo_200']:
        photo_file_name = str(data['id']) + '_vk.jpg'
        request.urlretrieve(data['photo_200'], str(MEDIA_USERS_IMAGE_PATH) + '/' + photo_file_name)
        user.image = 'users_image/' + photo_file_name

    user.save()
