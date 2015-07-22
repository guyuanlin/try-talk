from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from questions.models import UserLocationHistory


class Command(BaseCommand):

	args = '<amonut of days>'
	help = u'purge expired data'

	def handle(self, amount, *args, **options):
		try:
			amount = int(amount)
		except ValueError:
			print 'Amount must be a number'
			return

		threshold = timezone.now() - timedelta(days=amount)
		queryset = UserLocationHistory.objects.filter(
			create__lte=threshold
		)
		count = queryset.count()
		queryset.delete()
		print 'delete {0} user locations'.format(count)