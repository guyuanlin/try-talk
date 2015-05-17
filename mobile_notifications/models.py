# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxLengthValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

IOS_TYPE = 'ios'
ANDROID_TYPE = 'android'
DEVICE_TYPES = (
	(IOS_TYPE, IOS_TYPE),
	(ANDROID_TYPE, ANDROID_TYPE)
)


class Device(models.Model):

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		verbose_name=_('user'),
		help_text=_(u'使用者 ID'),
		blank=True,
		null=True
	)
	reg_id = models.CharField(
		max_length=250,
		verbose_name=_('registration id'),
		unique=True,
		help_text=_('registration id')
	)
	testing = models.BooleanField(
		verbose_name=_('testing device'),
		help_text=_('Push this device when testing'),
		default=False
	)

	class Meta:
		verbose_name = _('device')
		verbose_name_plural = _('devices')

	def __unicode__(self):
		return self.reg_id


class IOSDeviceManager(models.Manager):

	def testing_devices(self):
		return IOSDevice.objects.filter(
			testing=True
		)

	def for_user(self, user):
		return IOSDevice.objects.filter(
			user=user
		)


class IOSDevice(Device):

	objects = IOSDeviceManager()

	class Meta:
		verbose_name = _('iOS device')
		verbose_name_plural = _('iOS devices')


class AndroidDeviceManager(models.Manager):

	def testing_devices(self):
		return AndroidDevice.objects.filter(
			testing=True
		)

	def for_user(self, user):
		return AndroidDevice.objects.filter(
			user=user
		)


class AndroidDevice(Device):

	objects = AndroidDeviceManager()

	class Meta:
		verbose_name = _('anrdoid device')
		verbose_name_plural = _('android devices')


class History(models.Model):

	send_time = models.DateTimeField(
		verbose_name=_('send time'),
		auto_now_add=True
	)
	content = models.TextField(
		verbose_name=_('content'),
		validators=[MaxLengthValidator(300)]
	)

	class Meta:
		ordering = ('-send_time', '-id')
		verbose_name = _('history')
		verbose_name_plural = _('histories')

	def __unicode__(self):
		return self.content