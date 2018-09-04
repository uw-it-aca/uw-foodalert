from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
# Create your models here.


class Notification(models.Model):
    notification_id = models.CharField(max_length=40, default=None)
    location = models.CharField(max_length=40)
    event = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    content = JSONField()
    host = models.ForeignKey('Person')
    parent_notification = models.ForeignKey('Notification', default=None)
    host_permit_number = models.CharField(max_length=40, default=None)
    host_browser = models.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        food_list = self.foods.all()

    def json_data(self):
        return {
            "Notification": {
                "NotificationID": self.notification_id,
                "Location": self.location,
                "Event": self.event,
                "Host": self.host,
                "Created": self.created.isoformat() if (
                    self.created is not None) else None,
                "EndTime": self.end_time.isoformat() if (
                    self.end_time is not None) else None,
                "Content": self.content,
                "FoodList": self.food_list if (
                    self.food_list is not None) else None,
                "PermitNumber": self.host_permit_number if (
                    self.host_permit_number is not None) else None,

            }
        }


class Subscription(models.Model):
    net_id = models.CharField(max_length=40, default=None)
    sms_contact = models.CharField(max_length=20, default=None)
    email_contact = models.CharField(max_length=60, default=None)

    def json_data(self):
        return {
            "Subscription": {
                "NetID": self.net_id,
                "SMS": self.sms_contact,
                "Email": self.email_contact
            }
        }


class Person(models.Model):
    # Uses Django User model with an added "active_message" field
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active_message = models.CharField(max_length=40, default=None)

    def json_data(self):
        return {
            "Person": {
                "NetID": self.user.email,
                "ActiveMessage": self.active_message
            }
        }


class Foods(models.Model):
    notification = models.ManyToManyField(Notification, related_name='foods')
    food_name = models.CharField(max_length=30)
