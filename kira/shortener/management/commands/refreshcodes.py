from django.core.management.base import BaseCommand,CommandError
from shortener.models import KirrUrl

class Command(BaseCommand):
    help ='Refreshes all KirrUrl shortcodes'


    def handle(self,*args,**options):
        return KirrUrl.objects.refresh_shortcodes()
