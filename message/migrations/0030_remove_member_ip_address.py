# Generated by Django 4.1.4 on 2023-07-01 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0029_rename_groupname_member_group_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='ip_address',
        ),
    ]