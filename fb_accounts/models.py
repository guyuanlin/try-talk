# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _


class FacebookID(models.Model):

	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		verbose_name=_(u'使用者')
	)
	fb_id = models.CharField(
		max_length=200,
		verbose_name=_(u'使用者的 FB ID'),
		help_text=_(u'使用者的 FB ID')
	)

	def __unicode__(self):
		return self.fb_id

	class Meta:
		verbose_name = _(u'Facebook ID')
		verbose_name_plural = _(u'Facebook IDs')
		unique_together = ('fb_id',)