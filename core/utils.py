from itertools import imap
import uuid
from datetime import datetime
import os

from django.template.defaultfilters import slugify
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename
        if hasattr(instance, 'name') and instance.name:
            filename = '{}.{}'.format(slugify(instance.name[:255]), ext)
        elif hasattr(instance, 'title') and instance.title:
            filename = '{}.{}'.format(slugify(instance.title[:255]), ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(slugify(str(uuid.uuid4())), ext)
        # return the whole path to the file
        return os.path.join(self.path, "%s" % datetime.now().year, "%s" % datetime.now().month, filename)


def fake_users(number=10):
    last_id = 0
    last_user = User.objects.order_by('-pk').first()
    if last_user:
        last_id = last_user.id
    for i in range(last_id + 1, last_id + number):
        user_data = dict(first_name='User%dFirstName' % i,
                         last_name='User%dLastName' % i,
                         username='user%d' % i,
                         email='user%d@magendo.com' % i,
                         password='123456789',
                         )
        User.objects.create_user(**user_data)
    return "%s users created!" % number


def lists_overlap(a, b):
    sb = set(b)
    return any(imap(sb.__contains__, a))
