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


class LoginSerializer(serializers.ModelSerializer):

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
	auth_token = serializers.SerializerMethodField(
		help_text=_(u'使用者認證金鑰')
	)

	def get_auth_token(self, obj):
		try:
			return obj.auth_token.key
		except Token.DoesNotExist:
			token = Token.objects.create(user=obj)
			return token.key

	def validate(self, data):
		credentials = {
			'fb_id': data.get('fb_id')
		}
		if all(credentials.values()):
			user = authenticate(**credentials)
			if user and not user.is_active:
				msg = _(u'帳號未啟用')
				raise serializers.ValidationError(msg)
			return data
		else:
			msg = _(u'請輸入 Facebook ID')
			raise serializers.ValidationError(msg)

	def create(slef, validated_data):
		fb_id = validated_data.get('fb_id')
		device_type = validated_data.get('device_type')
		reg_id = validated_data.get('reg_id')

		fb_account, created = models.FacebookID.objects.get_or_create(fb_id=fb_id)
		user = fb_account.user
		if device_type and device_type == IOS_TYPE:
			device, created = IOSDevice.objects.get_or_create(
				reg_id=reg_id
			)
			device.user = user
			device.save()
		elif device_type and device_type == ANDROID_TYPE:
			device, created = AndroidDevice.objects.get_or_create(
				reg_id=reg_id
			)
			device.user = user
			device.save()
		return user

	class Meta:
		model = get_user_model()
		fields = ('fb_id', 'device_type', 'reg_id', 'auth_token')