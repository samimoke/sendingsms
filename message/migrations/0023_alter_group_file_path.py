# Generated by Django 4.1.4 on 2023-06-27 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0022_alter_group_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='file_path',
            field=models.FilePathField(path=None),
        ),
    ]
