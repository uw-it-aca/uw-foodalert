# Generated by Django 2.2.10 on 2020-02-11 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodalert', '0006_auto_20191206_2045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-created_time',)},
        ),
        migrations.AlterModelOptions(
            name='update',
            options={'ordering': ('created_time',)},
        ),
    ]
