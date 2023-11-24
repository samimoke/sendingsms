
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Deletes users who have been registered for 30 days or more.'

    def handle(self, *args, **options):
        thirty_days_ago = datetime.now() - timedelta(days=30)
        users_to_delete = User.objects.filter( is_superuser=False,date_joined__lte=thirty_days_ago)

        for user in users_to_delete:
            user.delete()

        self.stdout.write(f'{len(users_to_delete)} user(s) deleted successfully.')

