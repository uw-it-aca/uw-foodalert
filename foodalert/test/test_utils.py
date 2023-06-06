# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock

from django.contrib.auth.models import User
from django.test import Client

from twilio.request_validator import RequestValidator

from foodalert.models import Notification, Allergen, Update, FoodQualification
from foodalert.sender import TwilioSender, Sender


def create_notification_from_data(data, user):
    notif_obj = Notification.objects.create(
        location=data["location"],
        event=data["event"],
        end_time=datetime.strptime(data["end_time"] +
                                   "+0000", "%Y-%m-%dT%H:%M:%S.%fZ%z"),
        food_served=data["food_served"],
        bring_container=data["bring_container"],
        host=user,
        host_user_agent=data["userAgent"],
        ended=data["ended"])
    for allergen in data["allergens"]:
        notif_obj.allergens.add(Allergen.objects.get(name=allergen))
    for food_qualification in data["food_qualifications"]:
        notif_obj.food_qualifications.add(
            FoodQualification.objects.get(internalName=food_qualification)
        )
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


def create_user_from_data(data):
    user = User.objects.create_user(username=data["username"],
                                    email=data["email"],
                                    password=data["password"],
                                    is_active=1)
    return user


def create_client_with_mock_saml(user, member_of):
    client = Client()
    client.force_login(user)
    session = client.session
    session['samlUserdata'] = {"isMemberOf": member_of}
    session.save()

    return client


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


def generate_twilio_request_validator_mock():
    return patch.object(
        RequestValidator, 'validate',
        new_callable=PropertyMock,
        return_value=PropertyMock(return_value=True)
    )
