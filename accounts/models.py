# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token

from .utils import random_num_string


USERNAME_PREFIX = 'guest_'
PASSWORD_LENGTH = 10

class Guest(models.Model):

	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		verbose_name=_(u'使用者'),
		null=True,
		related_name='guest'
	)
	guest_id = models.CharField(
		max_length=20,
		verbose_name=_(u'試用者 ID'),
		help_text=_(u'試用者 ID'),
		unique=True,
		null=True,
		blank=True,
	)
	create = models.DateTimeField(
		verbose_name=_(u'建立時間'),
		auto_now_add=True,
		auto_now=False,
	)

	def __unicode__(self):
		return self.guest_id

	class Meta:
		ordering = ('-create',)
		verbose_name = _(u'試用者')
		verbose_name_plural = _(u'試用者')


# 沒有使用到，但未來可能會使用，先保留
class UserSettings(models.Model):
	pass


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)


@receiver(post_save, sender=Guest)
def create_order_receiver(sender, instance=None, created=False, **kwargs):
	if created:
		guest_id = '{0}{1:06d}'.format(
			instance.create.strftime('%Y%m%d%H%M%S'),
			instance.id % 1000000
		)
		instance.guest_id = guest_id

		if not instance.user:
			user = get_user_model()(
				username='{0}{1}'.format(USERNAME_PREFIX, guest_id)
			)
			user.set_password(random_num_string(PASSWORD_LENGTH))
			user.save()
			instance.user = user

		instance.save()