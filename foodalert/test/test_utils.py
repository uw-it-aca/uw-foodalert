from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock

from foodalert.models import Notification, Allergen, Update
from foodalert.sender import TwilioSender, Sender, AmazonSNSProvider


def create_notification_from_data(data, user):
    notif_obj = Notification.objects.create(
        location=data["location"],
        event=data["event"],
        end_time=datetime.strptime(data["end_time"] +
                                   "+0000", "%Y-%m-%dT%H:%M:%S.%fZ%z"),
        food_served=data["food_served"],
        amount_of_food_left=data["amount_of_food_left"],
        bring_container=data["bring_container"],
        host=user,
        host_user_agent=data["userAgent"],
        ended=data["ended"])
    for allergen in data["allergens"]:
        notif_obj.allergens.add(Allergen.objects.get(name=allergen))
    data["id"] = notif_obj.id
    data["created_time"] = notif_obj.created_time
    data["end_time"] = notif_obj.end_time
    data["host"] = user


def create_update_from_data(data, notifs):
    update_data = Update.objects.create(
        text=data["text"],
        parent_notification=Notification.objects.get(
            id=notifs[data["parent_notification_id"]]["id"]
        ),
    )
    data["id"] = update_data.id
    data["created_time"] = update_data.created_time


def generate_twilio_mock():
    ret = Mock()
    ret.body = ''
    ret.status = 200
    m2 = Mock()
    m2.notifications = Mock()
    m2.notifications.create = PropertyMock(return_value=ret)

    m1 = Mock()
    m1.notify = Mock()
    m1.notify.services = PropertyMock(return_value=m2)

    return patch.object(TwilioSender, 'c',
                        new_callable=PropertyMock, return_value=m1)


def generate_amazon_mock():
    ret = {
        'failed': [],
        'successful': ['test']
    }
    return patch.object(AmazonSNSProvider, 'send_message',
                        return_value=ret)
