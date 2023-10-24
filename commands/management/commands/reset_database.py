from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry

from adopt.models import AdoptionRequest
from cats.models import Cat

class Command(BaseCommand):
	help = "Restores the provided database to its original state"

	def handle(self, *args, **options):
		# Set all cats to not adopted again
		Cat.objects.all().update(is_adopted=False)

		# Remove all adoption requests from the database
		AdoptionRequest.objects.all().delete()

		# Delete the recent admin actions history
		LogEntry.objects.all().delete()