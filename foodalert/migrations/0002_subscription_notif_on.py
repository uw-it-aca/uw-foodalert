# Generated by Django 2.1 on 2019-07-16 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodalert', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='notif_on',
            field=models.BooleanField(default=False),
        ),
    ]
