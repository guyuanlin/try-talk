# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from . import models
from mobile_notifications.models import (
	IOSDevice,
	# AndroidDevice,
	DEVICE_TYPES,
	IOS_TYPE,
	# ANDROID_TYPE
)
from mobile_notifications.serializers import IOSRegIDMixin


class LoginSerializer(IOSRegIDMixin, serializers.ModelSerializer):

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
			return obj.user.auth_token.key
		except Token.DoesNotExist:
			token = Token.objects.create(user=obj.user)
			return token.key

	def validate_guest_id(self, value):
		if value:
			credentials = {'guest_id': value}
			user = authenticate(**credentials)
			if not user:
				msg = _(u'試用者不存在，請輸入空值重新註冊')
				raise serializers.ValidationError(msg)
			elif not user.is_active:
				msg = _(u'帳號已被停用')
				raise serializers.ValidationError(msg)
			return value
		return value

	def create(slef, validated_data):
		guest_id = validated_data.get('guest_id')
		device_type = validated_data.get('device_type')
		reg_id = validated_data.get('reg_id')

		if not guest_id:
			guest = models.Guest.objects.create()
		else:
			guest = models.Guest.objects.get(guest_id=guest_id)

		user = guest.user
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
		return guest

	class Meta:
		model = models.Guest
		fields = ('guest_id', 'device_type', 'reg_id', 'auth_token')
		extra_kwargs = {
			"guest_id": {
				"validators": [],
			},
		}