from datetime import datetime, timedelta

import dateutil.parser

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from django.contrib.auth.models import User
from foodalert.models import Notification, Update, Allergen, Subscription, \
    FoodQualification
from phonenumber_field.serializerfields import PhoneNumberField


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ['id', 'name']

    def create(self, validated_data):
        allergen = Allergen.objects.create()

        allergen.name = validated_data["name"]
        allergen.save()

        return allergen


class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('event', 'host', 'ended')
        read_only_fields = ['event', 'host', 'ended']

    def to_representation(self, notif):
        user = User.objects.get(pk=notif.host.id)
        return {
            'id': notif.id,
            'netID': user.username,
            'event': notif.event,
            'ended': notif.ended
        }


class NotificationDetailSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, required=False)

    class Meta:
        model = Notification
        fields = ('location', 'event', 'created_time',
                  'end_time', 'food_served',
                  'food_qualifications', 'host', 'bring_container',
                  'allergens', 'host_user_agent', 'ended')
        read_only_fields = ['created_time', 'end_time', 'host', 'ended']

    def create(self, validated_data):
        allergen_data = validated_data.pop('allergens')
        food_qualifications_data = validated_data.pop('food_qualifications')
        notif = Notification.objects.create(**validated_data)
        if allergen_data:
            for allergen in allergen_data:
                entry = Allergen.objects.get(name=allergen)
                notif.allergens.add(entry)
        if food_qualifications_data:
            for food_qualification in food_qualifications_data:
                entry = FoodQualification.objects.get(
                    internalName=food_qualification
                )
                notif.food_qualifications.add(entry)
        notif.save()
        return notif

    def to_representation(self, notif):
        user = User.objects.get(pk=notif.host.id)
        return {
            'id': notif.id,
            'netID': user.username,
            'location': notif.location,
            'event': notif.event,
            'time': {
                'created': notif.created_time,
                'end': notif.end_time,
            },
            'bring_container': notif.bring_container,
            'food': {
                'served': notif.food_served,
                'allergens': [x.name for x in notif.allergens.all()],
                'qualifications': [
                    x.internalName for x in notif.food_qualifications.all()
                ]
            },
            'userAgent': notif.host_user_agent,
            'ended': notif.ended
        }

    def to_internal_value(self, data):
        if not self.check_valid(data, "netID"):
            raise ValidationError({
                "Bad Request": "Post data must have a netID field"})
        if not self.check_valid(data, "location"):
            raise ValidationError({
                "Bad Request": "Post data must have a location field"})
        if not self.check_valid(data, "event"):
            raise ValidationError({
                "Bad Request": "Post data must have an event field"})
        if not self.check_valid(data, "end_time"):
            raise ValidationError({
                "Bad Request": "Post data must have a end_time field"})
        if not self.check_valid(data, "bring_container"):
            raise ValidationError({
                "Bad Request": "Post data must have a bring_container field"})
        if not self.check_valid(data, "food") or \
           not self.check_valid(data["food"], "served") or \
           not self.check_valid(data["food"], "qualifications"):
            raise ValidationError({
                "Bad Request": "Post data must have a proper food field"})
        if not self.check_valid(data, "host") or \
           not self.check_valid(data["host"], "userAgent"):
            raise ValidationError({
                "Bad Request": "Post data must have a host.userAgent field"})
        ret = {
            'location': data["location"],
            'event': data["event"],
            'food_served': data["food"]["served"],
            'bring_container': data["bring_container"],
            'allergens': None,
            'host_user_agent': data["host"]["userAgent"]
        }

        ret["created_time"] = datetime.now().astimezone()
        ret["end_time"] = dateutil.parser.parse(data["end_time"])

        if "allergens" in data["food"] and data["food"]["allergens"] != []:
            ret["allergens"] = data["food"]["allergens"]
            for allergen in ret["allergens"]:
                if not Allergen.objects.filter(
                    name=allergen
                ).exists():
                    raise ValidationError({
                        "Bad Request": "Allergen does not exist"
                    })

        if data["food"]["qualifications"] != []:
            ret["food_qualifications"] = data["food"]["qualifications"]
            for food_qualification in ret["food_qualifications"]:
                if not FoodQualification.objects.filter(
                    internalName=food_qualification
                ).exists():
                    raise ValidationError({
                        "Bad Request": "Food Qualification does not exist"
                    })

        return ret

    def check_valid(self, obj, field):
        return field in obj and obj[field] is not None and obj[field] != ""


class UpdateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ['id', 'parent_notification']

    def to_representation(self, update):
        return {
            "id": update.id,
            "parent_notification_id": update.parent_notification.id
        }


class UpdateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ('id', 'text', 'parent_notification', 'created_time')

    def to_representation(self, update):
        return {
            "id": update.id,
            "netID": update.parent_notification.host.username,
            "text": update.text,
            "parent_notification_id": update.parent_notification.id,
            "created_time": update.created_time
        }

    def to_internal_value(self, data):
        if not self.check_valid(data, "text"):
            raise ValidationError({
                "Bad Request": "Post data must have a valid text field"})
        if not self.check_valid(data, "parent_notification_id"):
            raise ValidationError({
                "Bad Request": "Post data must have a valid" +
                "parent_notification_id field"})

        ret = {
            'text': data['text']
        }

        try:
            ret['parent_notification'] = Notification.objects.get(
                                            pk=data['parent_notification_id'])
        except Notification.DoesNotExist:
            raise ValidationError({
                "Bad Request": "Bad notification ID"})
        if (ret['parent_notification'].ended):
            raise ValidationError({
                "Bad Request": "Parent notification has already ended"})
        if 'ended' in data and data['ended']:
            ret['parent_notification'].ended = True
            ret['parent_notification'].save()
        return ret

    def check_valid(self, obj, field):
        return field in obj and obj[field] is not None


class SubscriptionDetailSerializer(serializers.ModelSerializer):
    sms_number = PhoneNumberField(allow_blank=True)
    queryset = User.objects.all()

    class Meta:
        model = Subscription
        fields = ('id', 'netid', 'sms_number', 'number_verified', 'email',
                  'send_sms', 'email_verified', 'send_email')
        read_only_fields = ("number_verified", 'email_verified', 'email')

    def to_internal_value(self, data):
        obj = self.context['view'].get_object()
        ret = {
            'email_verified': obj.email_verified,
            'number_verified': obj.number_verified,
            'email': obj.email
        }
        if 'sms_number' in data:
            ret['sms_number'] = data['sms_number']
            if data['sms_number'] != obj.sms_number:
                ret['number_verified'] = False
                ret['send_sms'] = False
        if 'send_sms' in data:
            ret['send_sms'] = data['send_sms']
            if not ret['number_verified']:
                ret['send_sms'] = False
        if 'send_email' in data:
            ret['send_email'] = data['send_email']
            if not ret['email_verified']:
                ret['send_email'] = False
        return ret


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'netid', 'email', 'sms_number')

    def to_representation(self, update):
        r = self.context['request']._request.method
        if r == 'POST':
            return {
                "id": update.id,
                "netID": update.netid,
                "email": update.email,
                "email_verified": update.email_verified,
                "send_email": update.send_email,
                "sms_number": str(update.sms_number),
                "number_verified": update.number_verified,
                "send_sms": update.send_sms,
            }
        else:
            return {
                "id": update.id,
                "netID": update.netid,
            }

    def to_internal_value(self, data):
        if not self.check_valid(data, "email"):
            raise ValidationError({
                "Bad Request": "Post data must have a valid email field"})
        if not self.check_valid(data, "sms_number"):
            raise ValidationError({
                "Bad Request": "Post data must have a valid sms_number field"
                })
        if data['email'] != '':
            if not data['email'].endswith('@uw.edu'):
                raise ValidationError({
                    "Bad Request": "Email must be a UW email."
                    })
            user_netid = self.context['request'].user.username
            if not data['email'].startswith(user_netid):
                raise ValidationError({
                    "Bad Request": "Email must match netid"
                    })
        return data

    def check_valid(self, obj, field):
        return field in obj and obj[field] is not None
