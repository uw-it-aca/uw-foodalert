# Generated by Django 2.2.9 on 2020-02-21 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodalert', '0007_auto_20200211_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='twilio_stop',
            field=models.BooleanField(default=False),
        ),
    ]
