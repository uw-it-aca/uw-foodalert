# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-14 18:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodalert', '0010_auto_20190111_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='host_permit_number',
        ),
    ]
