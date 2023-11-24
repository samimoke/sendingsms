
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deletes users who registered 30 days ago, excluding superusers'

    def handle(self, *args, **options):
        threshold_date = timezone.now() - timezone.timedelta(days=30)
        users_to_delete = User.objects.filter(date_joined__lte=threshold_date, is_superuser=False)
        count = users_to_delete.count()
        users_to_delete.delete()
        self.stdout.write(f'Successfully deleted {count} users')

