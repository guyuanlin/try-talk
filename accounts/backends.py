# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from . import models


class GuestModelBackend(ModelBackend):

	def authenticate(self, guest_id=None, **kwargs):
		try:
			guest = models.Guest.objects.get(guest_id=guest_id)
			user = guest.user
			return user
		except models.Guest.DoesNotExist:
			# Run the default password hasher once to reduce the timing
			# difference between an existing and a non-existing user (#20760).
			UserModel = get_user_model()
			UserModel().set_password('fake_password')