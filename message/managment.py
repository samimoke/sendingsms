
from django.contrib.auth.management.commands.createsuperuser import Command as DefaultCreateSuperUserCommand
from django.contrib.auth.models import Group


class Command(DefaultCreateSuperUserCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)  # Call the default createsuperuser command
        
        group_name = 'Our Customers'
        default_group, _ = Group.objects.get_or_create(name=group_name)
        self.stdout.write(f"Created or retrieved the '{group_name}' group.")
        
from django.contrib.auth.management.commands.createsuperuser import Command as DefaultCreateSuperUserCommand
from django.contrib.auth.models import Group


class Command(DefaultCreateSuperUserCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)  # Call the default createsuperuser command
        
        default_group_name = 'Your Custom Group Name'
        default_group, _ = Group.objects.get_or_create(name=default_group_name)
        self.stdout.write(f"Created or retrieved the '{default_group_name}' group.")