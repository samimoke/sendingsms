# Generated by Django 4.1.4 on 2023-06-27 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0026_rename_mycontact_member_groupname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='ids',
            new_name='group_id',
        ),
    ]