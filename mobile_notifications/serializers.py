# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import ugettext as _

from . import models


class IOSDeviceSerializer(serializers.ModelSerializer):

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
