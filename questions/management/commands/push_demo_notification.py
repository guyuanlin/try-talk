import logging

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from questions.tasks import push_question_demo


logger = logging.getLogger(__name__)

class Command(BaseCommand):

	args = ''
	help = u'push fake notifications to all users'

	def handle(self, *args, **options):
		push_question_demo()
		logger.info('push fake notifications to all users completed at {0}'.format(timezone.now()))
		return
