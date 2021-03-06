# Generated by Django 2.1 on 2019-08-27 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodalert', '0002_subscription_notif_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='safe_foods',
        ),
        migrations.AddField(
            model_name='notification',
            name='food_qualification',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='amount_of_food_left',
            field=models.CharField(max_length=150),
        ),
        migrations.DeleteModel(
            name='SafeFood',
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='notif_on',
            new_name='send_email',
        ),
        migrations.AddField(
            model_name='subscription',
            name='send_sms',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='email_verified',
            field=models.BooleanField(default=True),
        ),
    ]
