from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from django.contrib.auth.models import User
from foodalert.models import Notification, Update, SafeFood, Allergen,\
        Subscription


class SafeFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafeFood
        fields = ('name')


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ('name')


class NotificationSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, required=False)
    safe_foods = SafeFoodSerializer(many=True, required=False)
    host = serializers.ReadOnlyField()

    class Meta:
        model = Notification
        fields = ('location', 'location_details', 'event', 'created_time',
                  'end_time', 'food_served', 'amount_of_food_left', 'host',
                  'bring_container', 'safe_foods', 'allergens',
                  'host_user_agent')

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
            'location': {
                'main': notif.location,
                'detail': notif.location_details,
            },
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
            }
        }

    def to_internal_value(self, data):
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
            'location': data["location"]["main"],
            'location_details': data["location"]["detail"],
            'event': data["event"],
            'created_time': data["time"]["created"],
            'end_time': data["time"]["ended"],
            'food_served': data["food"]["served"],
            'amount_of_food_left': data["food"]["amount"],
            'bring_container': data["bringContainers"],
            'safe_foods': None,
            'allergens': None,
            'host_user_agent': data["host"]["userAgent"],
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
            raise ValidaionError(
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


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'netid', 'sms_number', 'email')

    def to_internal_value(self, data):
        ret = {
            'email': data['email'],
            'sms_number': data['sms'],
        }

        if 'id' in data:
            ret['id'] = data['id']
            ret['user'] = Subscription.objects.get(pk=data['id']).user
        elif 'netId' in data:
            ret['user'] = User.objects.get(email=data['netId'])
        else:
            raise ValidationError({"netId": "must specify netid"})

        return ret
