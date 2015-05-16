# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from . import models


class FacebookIDModelBackend(ModelBackend):

	def authenticate(self, fb_id=None, **kwargs):
		try:
			fb_id_obj = models.FacebookID.objects.get(fb_id=fb_id)
			user = fb_id_obj.user
			return user
		except models.FacebookID.DoesNotExist:
			# Run the default password hasher once to reduce the timing
			# difference between an existing and a non-existing user (#20760).
			UserModel = get_user_model()
			UserModel().set_password('fake_password')