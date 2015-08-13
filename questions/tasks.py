# -*- coding: utf-8 -*-
import logging
from celery import shared_task

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.gis.measure import D

from mobile_notifications.models import IOSDevice
from mobile_notifications import senders
from questions.serializers import QuestionSerializer
from questions.models import UserLocationHistory, Question


# search distance(unit:km)
DISTANCE = 5

@shared_task
def push_question(question_data):
	alert = _(u'有人在您熟悉的位置發問囉！請點擊通知觀看問題描述！')
	custom_data = question_data
	question_id = question_data.get('id')
	try:
		question = Question.objects.get(id=question_id)
		now = timezone.now()
		center = question.location
		notify_user_ids = UserLocationHistory.objects.exclude(
			user__id=question.owner.id
		).filter(
			location__distance_lte=(center, D(m=(DISTANCE/100.0)))
		).order_by('user').distinct('user').values_list('user__id', flat=True)

		# apns
		devices = IOSDevice.objects.filter(
			user__id__in=notify_user_ids
		)
		notifications = []
		for device in devices:
			apns_notification = senders.APNSNotification(
				device=device,
				alert=alert,
				badge=1,
				custom=custom_data
			)
			notifications.append(apns_notification)
		senders.apns_send(notifications)
	except Question.DoesNotExist:
		logging.exception('question id {0} does not exist'.format(question_id))