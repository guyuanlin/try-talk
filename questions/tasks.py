# -*- coding: utf-8 -*-
import logging
import json
from celery import shared_task

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.gis.measure import D

from mobile_notifications.models import IOSDevice
from mobile_notifications import senders
from questions.serializers import QuestionSerializer
from questions.models import UserLocationHistory, Question

logger = logging.getLogger(__name__)

# search distance(unit:km)
DISTANCE = getattr(settings, 'PUSH_RANGE', 10)

def truncat_with_dots(content, length=100):
	if len(content) > length:
		return content[:(length - 3)] + u'...'
	return content

@shared_task
def push_question(question_json):
	question_data = json.loads(question_json)
	alert = _(u'[發問]') + truncat_with_dots(question_data['content'])
	question_id = question_data['id']
	custom_data = {
		'id': question_id,
	}
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
				custom=custom_data,
			)
			notifications.append(apns_notification)
		logger.debug('push to registration ids: {0}'.format(notifications))
		senders.apns_send(notifications)
	except Question.DoesNotExist:
		logger.exception('question id {0} does not exist'.format(question_id))


# for demo, push to all users
@shared_task
def push_question_demo():
	alert = _(u'有人在距離您 2 公里的位置發問，他需要你的幫助！')
	try:
		UserModel = get_user_model()
		notify_user_ids = UserModel.objects.all().values_list('id', flat=True)

		# apns
		devices = IOSDevice.objects.filter(
			user__id__in=notify_user_ids
		)
		notifications = []
		for device in devices:
			logger.debug('push to device {0}'.format(device))
			apns_notification = senders.APNSNotification(
				device=device,
				alert=alert,
				badge=1,
				custom={},
			)
			notifications.append(apns_notification)
		senders.apns_send(notifications)
	except:
		logger.exception('push notification failed')