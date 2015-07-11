# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from . import models


class TwitterIDModelBackend(ModelBackend):

	def authenticate(self, twitter_id=None, **kwargs):
		try:
			twitter_id_obj = models.TwitterID.objects.get(twitter_id=twitter_id)
			user = twitter_id_obj.user
			return user
		except models.TwitterID.DoesNotExist:
			# Run the default password hasher once to reduce the timing
			# difference between an existing and a non-existing user (#20760).
			UserModel = get_user_model()
			UserModel().set_password('fake_password')