# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-11 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodalert', '0009_auto_20190111_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='host_user_agent',
            field=models.TextField(),
        ),
    ]