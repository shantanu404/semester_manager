# Generated by Django 3.2 on 2021-05-22 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20210501_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='special',
            field=models.BooleanField(default=True),
        ),
    ]
