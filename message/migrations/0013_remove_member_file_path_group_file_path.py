# Generated by Django 4.1.4 on 2023-06-26 12:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0012_member_file_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='file_path',
        ),
        migrations.AddField(
            model_name='group',
            name='file_path',
            field=models.FilePathField(default=django.utils.timezone.now, max_length=200, path='C:/Users/SAMUEL PC/Downloads\\Debo/Debo/sms/sendsms/message/upload/sms.txt'),
            preserve_default=False,
        ),
    ]
