# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

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

	id = serializers.IntegerField(
		read_only=True,
		help_text=_(u'問題 ID'),
	)
	tags = TagSlugRelatedField(
		many=True,
		slug_field='name',
		queryset=models.Tag.objects.all(),
		help_text=_(u'關鍵字，型態為 array(string)'),
	)
	reply_count = serializers.IntegerField(
		read_only=True,
		help_text=_(u'回覆數量'),
	)
	time_info = serializers.SerializerMethodField(
		help_text=_(u'時間資訊，型別為 JSON object，包含 time(string) 與 display(string) 欄位'),
	)

	def validate_tags(self, value):
		if value and len(value) > MAX_TAG_COUNT:
			raise serializers.ValidationError(_(u'關鍵字不能多於 4 個'))
		return value

	def get_time_info(self, obj):
		update_time = obj.update
		now = timezone.now()
		delta = now - update_time
		if delta.days > 0:
			display = _(u'%(days)d天前發布') % {'days': delta.days}
		elif delta.seconds > 3600:
			display = _(u'%(hours)d小時前發布') % {'hours': (delta.seconds / 3600)}
		elif delta.seconds > 60:
			display = _(u'%(minutes)d分鐘前發布') % {'minutes': (delta.seconds / 60)}
		else:
			display = _(u'%(seconds)d秒前發布') % {'seconds': delta.seconds}
		return {
			'time': update_time,
			'display': display,
		}

	class Meta:
		model = models.Question
		fields = ('id', 'category', 'content', 'location', 'tags', 'reply_count', 'time_info')