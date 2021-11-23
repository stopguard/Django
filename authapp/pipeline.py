from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils.timezone import now
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'interests',
                                                                 'personal', 'domain', 'photo_max_orig')),
                                                access_token=response['access_token'],
                                                v='5.131')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    sex = data.get('sex', '')
    if sex:
        user.userprofile.gender = UserProfile.MALE if sex == 2 else UserProfile.FEMALE

    about = data.get('about', '')
    if about:
        user.userprofile.about_me = about

    data_bdate = data.get('bdate', '')
    if data_bdate:
        bdate = datetime.strptime(data_bdate, '%d.%m.%Y').date()

        age = now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    interests = data.get('interests', '')
    if interests:
        user.userprofile.tagline = interests

    personal = data.get('personal', {})
    langs = ', '.join(personal.get('langs', ''))
    if langs:
        user.userprofile.about_me += f'\nЯзыки: {langs}'

    domain = data.get('domain', '')
    if domain:
        user.userprofile.about_me += f'\nhttps://vk.com/{domain}/'

    photo_max_orig = data.get('photo_max_orig', '')
    if photo_max_orig:
        user.avatar = photo_max_orig

    user.save()
