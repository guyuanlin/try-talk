# -*- coding: utf-8 -*-
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import ugettext as _

from . import models


IOS_REG_ID_REGEX = '[0-9a-f]{64}'

class IOSRegIDMixin(object):

	def validate_reg_id(self, value):
		if value:
			value = value.strip()
			match_result = re.match(IOS_REG_ID_REGEX, value)
			if not match_result:
				msg = 'invalid registration id'
				raise serializers.ValidationError(msg)
		return value

	def validate(self, data):
		device_type = data.get('device_type', None)
		reg_id = data.get('reg_id', None)

		if bool(device_type) ^ bool(reg_id):
			msg = _(u'device_type 與 reg_id 必須同時設定，不能只設定其中一個')
			raise serializers.ValidationError(msg)
		return data


class IOSDeviceSerializer(IOSRegIDMixin, serializers.ModelSerializer):

	user = serializers.PrimaryKeyRelatedField(
		help_text=_(u'使用者 ID'),
		read_only=True
	)

	def create(self, validated_data):
		reg_id = validated_data['reg_id']
		user = validated_data['user']
		device = models.IOSDevice.objects.create(
			reg_id=reg_id,
			user=user
		)
		return device

	def update(self, instance, validated_data):
		user = validated_data['user']
		instance.user = user
		instance.save()
		return instance

	class Meta:
		model = models.IOSDevice
		fields = ('reg_id', 'user')


class AndroidDeviceSerializer(serializers.ModelSerializer):

	user = serializers.PrimaryKeyRelatedField(
		help_text=_(u'使用者 ID'),
		read_only=True
	)

	def create(self, validated_data):
		reg_id = validated_data['reg_id']
		user = validated_data['user']
		try:
			device = models.AndroidDevice.objects.get(
				reg_id=reg_id
			)
			device.user = user
			device.save()
		except models.AndroidDevice.DoesNotExist:
			device = models.AndroidDevice.objects.create(
				reg_id=reg_id,
				user=user
			)
		return device

	class Meta:
		model = models.AndroidDevice
		fields = ('reg_id', 'user')
