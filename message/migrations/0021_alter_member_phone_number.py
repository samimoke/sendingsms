# Generated by Django 4.1.4 on 2023-06-26 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0020_alter_member_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone_number',
            field=models.IntegerField(),
        ),
    ]
