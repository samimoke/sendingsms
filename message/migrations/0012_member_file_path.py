# Generated by Django 4.1.4 on 2023-06-26 12:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0011_remove_group_group_alter_member_mycontact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='file_path',
            field=models.FilePathField(default=django.utils.timezone.now, max_length=200, path='C:/Users/SAMUEL PC/Downloads\\Debo/Debo/sms/sendsms/message/upload/sms.txt'),
            preserve_default=False,
        ),
    ]
