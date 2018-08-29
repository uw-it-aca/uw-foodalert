from django.db import models

# Create your models here.


class Notification(models.Model):
    notification_id = models.CharField(max_length=40, default=None)
    location = models.CharField(max_length=40)
    event = models.CharField(max_length=40)
    created = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        self.message = {}
        self.food_list = []

    def json_data(self):
        return {
            "Notification": {
                "NotificationID": self.notification_id,
                "Location": self.location,
                "Event": self.event,
                "CreatedBy": self.created_by,
                "Created": self.created.isoformat() if (
                    self.created is not None) else None,
                "EndTime": self.end_time.isoformat() if (
                    self.end_time is not None) else None,
                "Message": self.message,
                "FoodList": self.food_list
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


class User(models.Model):
    active_message = models.CharField(max_length=40, default=None)

    def json_data(self):
        return {
            "User": {
                "ActiveMessage": self.active_message
            }
        }
