from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from django.contrib.auth.models import User
from foodalert.models import Notification, Update, SafeFood, Allergen,\
        Subscription
from phonenumber_field.serializerfields import PhoneNumberField


class SafeFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafeFood
        fields = ['name']


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ['id', 'name']

    def create(self, validated_data):
        allergen = Allergen.objects.create()

        allergen.name = validated_data["name"]
        allergen.save()

        return allergen


class NotificationSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, required=False)
    safe_foods = SafeFoodSerializer(many=True, required=False)
    host = serializers.ReadOnlyField()

    class Meta:
        model = Notification
        fields = ('location', 'event', 'created_time',
                  'end_time', 'food_served', 'amount_of_food_left', 'host',
                  'bring_container', 'safe_foods', 'allergens',
                  'host_user_agent', 'ended')

    def create(self, validated_data):
        allergen_data = validated_data.pop('allergens')
        safe_food_data = validated_data.pop('safe_foods')
        notif = Notification.objects.create(**validated_data)
        notif.save()
        if (allergen_data is not None):
            for allergen in allergen_data:
                entry = Allergen.objects.get(name=allergen)
                notif.allergens.add(entry)
        if (safe_food_data is not None):
            for safe_food in safe_food_data:
                entry = SafeFood.objects.get(name=safe_food)
                notif.safe_foods.add(entry)
        return notif

    def to_representation(self, notif):
        user = User.objects.get(pk=notif.host.id)
        return {
            'id': str(notif.id),
            'location': notif.location,
            'event': notif.event,
            'time': {
                'created': notif.created_time,
                'ended': notif.end_time,
            },
            'food': {
                'served': notif.food_served,
                'amount': notif.amount_of_food_left,
                'allergens': [x.name for x in notif.allergens.all()],
            },
            'bringContainers': notif.bring_container,
            'foodServiceInfo': {
                'safeToShareFood': [x.name for x in notif.safe_foods.all()],
            },
            'host': {
                'hostID': notif.host.id,
                'netID': user.username,
                'userAgent': notif.host_user_agent,
            },
            'ended': notif.ended
        }

    def to_internal_value(self, data):
        if 'ended' not in data:
            data["ended"] = False
        if data["ended"]:
            return {'ended': data["ended"]}
        if 'location' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a location field"})
        if 'event' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have an event field"})
        if 'time' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a time field"})
        if 'food' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a food field"})
        if 'foodServiceInfo' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a foodServiceInfo field"})
        if 'bringContainers' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a bringContainers field"})
        ret = {
            'location': data["location"],
            'event': data["event"],
            'created_time': data["time"]["created"],
            'end_time': data["time"]["ended"],
            'food_served': data["food"]["served"],
            'amount_of_food_left': data["food"]["amount"],
            'bring_container': data["bringContainers"],
            'safe_foods': None,
            'allergens': None,
            'host_user_agent': data["host"]["userAgent"],
            'ended': data["ended"]
        }
        if data["foodServiceInfo"]["safeToShareFood"] != []:
            ret["safe_foods"] = data["foodServiceInfo"]["safeToShareFood"]
        if data["food"]["allergens"] != []:
            ret["allergens"] = data["food"]["allergens"]
        if ret["end_time"] == "":
            raise ValidationError({"end_time": "Invalid Datetime format"})
        if ret["location"] == "":
            raise ValidationError({"location": "A location must be provided"})
        if ret["event"] == "":
            raise ValidationError({"event": "An event must be provided"})
        if ret["food_served"] == "":
            raise ValidationError(
                {"food_served": "At least one food served is required"})
        if ret["amount_of_food_left"] == "":
            raise ValidationError(
                {"amount_of_food_left": "Food amounts must be specified"})
        if ret["host_user_agent"] == "":
            raise ValidationError(
                {"host_user_agent": "User agent information is required"})
        return ret


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ('text', 'parent_notification', 'created_time')

        def to_internal_value(self, data):
            ret = {
                'text': data['text']
            }

            ret['parent_notification'] = Notification.objects.get(
                                         pk=data['parent_notification'])
            return ret


class SubscriptionDetailSerializer(serializers.ModelSerializer):
    sms_number = PhoneNumberField(allow_blank=True)

    class Meta:
        model = Subscription
        fields = ('id', 'netid', 'sms_number', 'number_verified', 'email',
                  'email_verified', 'notif_on')
        read_only_fields = ("number_verified", 'email_verified', 'notif_on')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'netid')

    def to_internal_value(self, data):
        ret = {
            'email': '',
            'sms_number': '',
            'notif_on': '',
        }

        if 'email' in data:
            ret['email'] = data['email']
        else:
            ret['email'] = ''

        if 'sms_number' in data:
            ret['sms_number'] = data['sms_number']
        else:
            ret['sms_number'] = ''

        if 'notif_on' in data:
            ret['notif_on'] = data['notif_on']
        else:
            ret['notif_on'] = False

        return data

    def create(self, validated_data):
        sub, created = Subscription.objects.get_or_create(
            user=self.context.get('request').user)

        sub.email = validated_data["email"]
        sub.sms_number = validated_data["sms_number"]
        sub.notif_on = False

        sub.save()

        return sub
