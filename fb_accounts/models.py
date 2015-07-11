# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

from accounts.utils import random_num_string


USERNAME_PREFIX = 'fb_'
PASSWORD_LENGTH = 10

class FacebookID(models.Model):

	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		verbose_name=_(u'使用者'),
	)
	fb_id = models.CharField(
		max_length=200,
		verbose_name=_(u'使用者的 FB ID'),
		help_text=_(u'使用者的 FB ID')
	)
	create = models.DateTimeField(
		verbose_name=_(u'建立時間'),
		auto_now_add=True,
		auto_now=False,
	)

	def __unicode__(self):
		return self.fb_id

	def save(self, *args, **kwargs):
		if not self.pk:		
			user = get_user_model()(
				username='{0}{1}'.format(USERNAME_PREFIX, self.fb_id)
			)
			user.set_password(random_num_string(PASSWORD_LENGTH))
			user.save()
			self.user = user
		return super(FacebookID, self).save(*args, **kwargs)

	class Meta:
		ordering = ('-create',)
		verbose_name = _(u'Facebook 使用者')
		verbose_name_plural = _(u'Facebook 使用者')
		unique_together = ('fb_id',)
