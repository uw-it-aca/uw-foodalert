# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-18 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodalert', '0012_remove_notification_host_permit_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='ended',
            field=models.BooleanField(default=False),
        ),
    ]