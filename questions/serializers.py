# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer

from . import models


class TagSlugRelatedField(serializers.SlugRelatedField):

	def to_internal_value(self, data):
		try:
			tag, create = self.get_queryset().get_or_create(**{self.slug_field: data})
			return tag
		except ObjectDoesNotExist:
			self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
		except (TypeError, ValueError):
			self.fail('invalid')


MAX_TAG_COUNT = 4

class QuestionSerializer(GeoModelSerializer):

	# tags = TagSerializer(many=True)
	tags = TagSlugRelatedField(
		many=True,
		slug_field='name',
		queryset=models.Tag.objects.all(),
	)

	def validate_tags(self, value):
		if value and len(value) > MAX_TAG_COUNT:
			raise serializers.ValidationError(_(u'關鍵字不能多於 4 個'))
		return value

	class Meta:
		model = models.Question
		fields = ('category', 'content', 'location', 'tags',)