# Generated by Django 4.1.4 on 2023-07-01 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0030_remove_member_ip_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reciever', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=50)),
            ],
        ),
    ]
