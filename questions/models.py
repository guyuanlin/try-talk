# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_delete
from django.db.models import F
from django.dispatch import receiver


FOOD = 'food'
SHOP = 'shop'
LOCATION = 'location'
OTHER = 'other'
CATEGORIES = (
	(FOOD, FOOD),
	(SHOP, SHOP),
	(LOCATION, LOCATION),
	(OTHER, OTHER),
)

CONTENT_MAX_LENGTH = 500


class Tag(models.Model):

	name = models.CharField(
		max_length=50,
		verbose_name=_(u'關鍵字'),
		unique=True,
		blank=False,
	)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _(u'關鍵字')
		verbose_name_plural = _(u'關鍵字')


class QuestionManager(models.GeoManager):

	def active(self):
		return Question.objects.filter(is_active=True)


class Question(models.Model):

	objects = QuestionManager()

	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		verbose_name=_(u'發問者'),
	)
	category = models.CharField(
		max_length=30,
		verbose_name=_(u'分類'),
		help_text=_(u'問題分類'),
		choices=CATEGORIES,
	)
	content = models.TextField(
		verbose_name=_(u'內容'),
		help_text=_(u'內容'),
		validators=[MaxLengthValidator(CONTENT_MAX_LENGTH)],
	)
	location = models.PointField(
		verbose_name=_(u'發問位置'),
		help_text=_(u'發問位置'),
	)
	tags = models.ManyToManyField(
		Tag,
		verbose_name=_(u'標籤'),
	)
	reply_count = models.IntegerField(
		verbose_name=_(u'回覆數'),
		default=0,
	)
	is_active = models.BooleanField(
		verbose_name=_(u'有效'),
		default=True,
	)
	create = models.DateTimeField(
		verbose_name=_(u'建立時間'),
		auto_now_add=True,
		auto_now=False,
	)
	update = models.DateTimeField(
		verbose_name=_(u'更新時間'),
		auto_now_add=False,
		auto_now=True,
	)

	def __unicode__(self):
		return self.content

	class Meta:
		ordering = ('-create',)
		verbose_name = _(u'問題列表')
		verbose_name_plural = _(u'問題列表')


class Reply(models.Model):

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		verbose_name=_(u'回覆者'),
	)
	question = models.ForeignKey(
		Question,
		verbose_name=_(u'所屬問題'),
		related_name='replys',
	)
	content = models.TextField(
		verbose_name=_(u'內容'),
		validators=[MaxLengthValidator(CONTENT_MAX_LENGTH)],
	)
	likes = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		verbose_name=_(u'按讚使用者'),
		related_name='like_replys',
	)
	is_active = models.BooleanField(
		verbose_name=_(u'有效'),
		default=True,
	)
	create = models.DateTimeField(
		verbose_name=_(u'建立時間'),
		auto_now_add=True,
		auto_now=False,
	)
	update = models.DateTimeField(
		verbose_name=_(u'更新時間'),
		auto_now_add=False,
		auto_now=True,
	)

	def like_count(self):
		return self.likes.count()
	like_count.short_description = _(u'按讚數')

	def __unicode__(self):
		return self.content

	class Meta:
		verbose_name = _(u'問題回覆')
		verbose_name_plural = _(u'問題回覆')


@receiver(post_save, sender=Reply)
def save_reply_receiver(sender, instance=None, created=False, **kwargs):
	if created:
		question = instance.question
		question.reply_count = F('reply_count') + 1
		question.save()


@receiver(pre_delete, sender=Reply)
def delete_reply_receiver(sender, instance=None, **kwargs):
	question = instance.question
	question.reply_count = F('reply_count') - 1
	question.save()