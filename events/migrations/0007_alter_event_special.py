# Generated by Django 3.2 on 2021-05-22 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='special',
            field=models.BooleanField(default=False),
        ),
    ]
