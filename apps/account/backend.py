# # -*- coding: utf-8 -*-

import json
import re
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from apps.account.models import User


class CasBackend(ModelBackend):
    def authenticate(self, openid):
        try:
            return User.objects.get(openid=openid)
        except ObjectDoesNotExist:
            return None