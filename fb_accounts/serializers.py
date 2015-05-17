# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework.authtoken.models import Token

from . import models
from mobile_notifications.models import (
	IOSDevice,
	AndroidDevice,
	DEVICE_TYPES,
	IOS_TYPE,
	ANDROID_TYPE
)


class LoginSerializer(serializers.Serializer):

	id = serializers.IntegerField(
		read_only=True,
		help_text=_(u'使用者 ID')
	)
	fb_id = serializers.CharField(
		write_only=True,
		required=True,
		allow_null=False,
		help_text=_(u'使用者的 FB ID')
	)
	device_type = serializers.ChoiceField(
		write_only=True,
		choices=DEVICE_TYPES,
		required=False,
		help_text=_(u'裝置類型')
	)
	reg_id = serializers.CharField(
		write_only=True,
		allow_blank=True,
		required=False,
		help_text=_(u'裝置註冊序號')
	)
	auth_token = serializers.CharField(
		read_only=True,
		help_text=_(u'認證金鑰')
	)
	is_registered = serializers.BooleanField(
		read_only=True,
		help_text=_(u'識別此 Facebook ID 是否已註冊')
	)

	def validate(self, data):
		"""
		驗證 facebook id 是否已註冊過
		"""
		credentials = {
			'fb_id': data.get('fb_id')
		}
		if all(credentials.values()):
			user = authenticate(**credentials)
			data['id'] = -1
			data['auth_token'] = None
			data['is_registered'] = False
				
			if user:
				if not user.is_active:
					msg = _(u'帳號未啟用')
					raise serializers.ValidationError(msg)
				data['id'] = user.id
				data['is_registered'] = True
				try:
					data['auth_token'] = user.auth_token.key
				except Token.DoesNotExist:
					pass
			return data
		else:
			msg = _(u'必須輸入 Facebook ID')
			raise serializers.ValidationError(msg)

	def create(slef, validated_data):
		fb_id = validated_data.get('fb_id')
		device_type = validated_data.get('device_type')
		reg_id = validated_data.get('reg_id')
		try:
			device = None
			user = models.FacebookID.objects.get(fb_id=fb_id).user
			if device_type and device_type == IOS_TYPE:
				device, created = IOSDevice.objects.get_or_create(
					reg_id=reg_id
				)
			elif device_type and device_type == ANDROID_TYPE:
				device, created = AndroidDevice.objects.get_or_create(
					reg_id=reg_id
				)
			if device:
				device.user = user
				device.save()
			return user
		except models.FacebookID.DoesNotExist:
			msg = _(u'Facebook ID "%s" 不存在' % fb_id)
			raise ValueError(msg)