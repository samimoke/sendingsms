# Generated by Django 4.1.4 on 2023-06-26 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0016_alter_group_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='file_path',
            field=models.FilePathField(max_length=200, path='C:/Users/SAMUEL PC/Downloads/Debo/Debo/sms/sendsms/message/upload/sms.txt'),
        ),
    ]
