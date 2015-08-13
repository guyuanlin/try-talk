# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.gis.geos import fromstr

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


class TimeInfoMixin(object):

	def get_time_info(self, obj):
		update_time = obj.update
		now = timezone.now()
		delta = now - update_time
		
		if delta.days > 30:
			display = _(u'%(months)d月前更新') % {'months': (delta.days / 30)}
		elif delta.days > 0:
			display = _(u'%(days)d天前更新') % {'days': delta.days}
		elif delta.seconds > 3600:
			display = _(u'%(hours)d小時前更新') % {'hours': (delta.seconds / 3600)}
		elif delta.seconds > 60:
			display = _(u'%(minutes)d分鐘前更新') % {'minutes': (delta.seconds / 60)}
		else:
			display = _(u'%(seconds)d秒前更新') % {'seconds': delta.seconds}
		return {
			'time': update_time,
			'display': display,
		}


MAX_TAG_COUNT = 4
GEOS_SRID = 4326
USER_LOCATION_KEY = 'location'

class QuestionSerializer(TimeInfoMixin, GeoModelSerializer):

	id = serializers.IntegerField(
		read_only=True,
		help_text=u'問題 ID',
	)
	tags = TagSlugRelatedField(
		many=True,
		slug_field='name',
		queryset=models.Tag.objects.all(),
		help_text=u'關鍵字，型態為 array(string)',
	)
	reply_count = serializers.IntegerField(
		read_only=True,
		help_text=u'回覆數量',
	)
	time_info = serializers.SerializerMethodField(
		help_text=u'時間資訊，型別為 JSON object，包含 time(string) 與 display(string) 欄位',
	)
	distance_info = serializers.SerializerMethodField(
		help_text=u'距離資訊，型別為 JSON object，包含 distance(integer, 單位為公里) 與 display(string) 欄位',
	)
	can_delete = serializers.SerializerMethodField(
		help_text=u'標示登入使用者是否可以刪除此問題'
	)

	def validate_tags(self, value):
		if value and len(value) > MAX_TAG_COUNT:
			raise serializers.ValidationError(_(u'關鍵字不能多於 4 個'))
		return value

	def get_distance_info(self, obj):
		if USER_LOCATION_KEY in self.context['request'].query_params:
			location_str = self.context['request'].query_params[USER_LOCATION_KEY]
			location_pnt = fromstr(location_str, srid=GEOS_SRID)
			distance = location_pnt.distance(obj.location) * 100.0
		else:
			distance = 0

		if distance < 1.0:
			display = _(u'距離%(distance)d公尺') % {'distance': int(distance * 1000.0)}
		else:
			display = _(u'距離%(distance)d公里') % {'distance': int(distance)}

		return {
			'distance': distance,
			'display': display,
		}

	def get_can_delete(self, obj):
		login_user = self.context['request'].user
		if login_user.pk == obj.owner.pk:
			return True
		return False

	def create(self, validated_data):
		question = super(QuestionSerializer, self).create(validated_data)
		# store the user location
		models.UserLocationHistory.objects.create(
			user=question.owner,
			location=question.location,
		)
		return question

	class Meta:
		model = models.Question
		fields = (
			'id', 'category', 'content', 'location',
			'tags', 'reply_count', 'time_info', 'distance_info',
			'can_delete'
		)


class ReplySerializer(TimeInfoMixin, serializers.ModelSerializer):

	like_count = serializers.SerializerMethodField(
		help_text=u'按讚數'
	)
	time_info = serializers.SerializerMethodField(
		help_text=u'時間資訊，型別為 JSON object，包含 time(string) 與 display(string) 欄位',
	)
	can_delete = serializers.SerializerMethodField(
		help_text=u'標示登入使用者是否可以刪除此回覆'
	)
	is_like = serializers.SerializerMethodField(
		help_text=u'登入的使用者是否有按過讚'
	)

	def get_like_count(self, obj):
		return obj.like_count()

	def get_can_delete(self, obj):
		login_user = self.context['request'].user
		if login_user.pk == obj.question.owner.pk or login_user.pk == obj.user.pk:
			return True
		return False

	def get_is_like(self, obj):
		login_user = self.context['request'].user
		return obj.likes.filter(id=login_user.id).exists()

	def create(self, validated_data):
		reply = super(ReplySerializer, self).create(validated_data)

		location = validated_data.get('location', None)
		if location:
			# store the user location
			models.UserLocationHistory.objects.create(
				user=reply.user,
				location=reply.location,
			)
		return reply

	class Meta:
		model = models.Reply
		fields = ('id', 'content', 'like_count', 'is_like', 'time_info', 'location', 'can_delete')