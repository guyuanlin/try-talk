# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer

from . import models


class TagSerializer(serializers.ModelSerializer):

	def validate_name(self, value):
		if not value:
			raise serializers.ValidationError(_(u'標籤名稱不能為空白'))
		return value

	def create(self, validated_data):
		name = validated_data.get('name')
		tag, created = models.Tag.objects.get_or_create(name=name)
		return tag

	class Meta:
		model = models.Tag
		fields = ('name',)
		extra_kwargs = {
			"guest_id": {
				"validators": [],
			},
		}


class QuestionSerializer(GeoModelSerializer):

	tags = TagSerializer(many=True)

	def create(self, validated_data):
		# fixme
		print validated_data
		return None

	class Meta:
		model = models.Question
		fields = ('category', 'content', 'location', 'tags',)