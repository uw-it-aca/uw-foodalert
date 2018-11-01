from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from django.contrib.auth.models import User
from foodalert.models import Notification, Update, SafeFood, Allergen,\
        Subscription


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('location', 'location_details', 'event', 'created_time',
                  'end_time', 'food_served', 'amount_of_food_left', 'host',
                  'bring_container', 'safe_foods', 'allergens',
                  'host_permit_number', 'host_user_agent')

    def to_representation(self, notification):
        return {
            'id': str(notification.id),
            'location': {
                'main': notification.location,
                'detail': notification.location_details,
            },
            'event': notification.event,
            'time': {
                'created': notification.created_time,
                'ended': notification.end_time,
            },
            'food': {
                'served': notification.food_served,
                'amount': notification.amount_of_food_left,
                'allergens': notification.allergens,
            },
            'bringContainers': notification.bring_container,
            'foodServiceInfo': {
                'permitNumber': notification.host_permit_number,
                'safeToShareFood': notification.safe_foods,
            },
            'host': {
                'hostID': notification.host.id,
                'netID': notification.host.email,
                'userAgent': notification.host_user_agent,
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
        if 'host' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a host field"})
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
            'host': User.objects.get(id=data["host"]["hostID"]),
            'bring_container': data["bringContainers"],
            'safe_foods': data["foodServiceInfo"]["safeToShareFood"],
            'allergens': data["food"]["allergens"],
            'host_permit_number': data["foodServiceInfo"]["permitNumber"],
            'host_user_agent': data["host"]["userAgent"],
        }
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
        fields = ('text', 'parent_notification')


class SafeFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafeFood
        fields = ('notification', 'name')


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ('notification', 'name')

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields= ('id', 'netid', 'sms_number', 'email')
