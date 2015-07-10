# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

from accounts.utils import random_num_string


USERNAME_PREFIX = 'twitter_'
PASSWORD_LENGTH = 10

class TwitterID(models.Model):

	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		verbose_name=_(u'使用者'),
	)
	twitter_id = models.CharField(
		max_length=200,
		verbose_name=_(u'使用者的 Twitter ID'),
		help_text=_(u'使用者的 Twitter ID'),
		unique=True,
	)

	def __unicode__(self):
		return self.twitter_id

	def save(self, *args, **kwargs):
		if not self.pk:		
			user = get_user_model()(
				username='{0}{1}'.format(USERNAME_PREFIX, self.twitter_id)
			)
			user.set_password(random_num_string(PASSWORD_LENGTH))
			user.save()
			self.user = user
		return super(TwitterID, self).save(*args, **kwargs)

	class Meta:
		verbose_name = _(u'Twitter ID')
		verbose_name_plural = _(u'Twitter IDs')