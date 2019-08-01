from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from django.contrib.auth.models import User
from foodalert.models import Notification, Update, Allergen, Subscription
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
                  'end_time', 'food_served', 'amount_of_food_left', 'host',
                  'bring_container', 'allergens', 'host_user_agent', 'ended')
        read_only_fields = ['created_time', 'end_time', 'host', 'ended']

    def create(self, validated_data):
        allergen_data = validated_data.pop('allergens')
        notif = Notification.objects.create(**validated_data)
        notif.save()
        for allergen in [] if not allergen_data else allergen_data:
            entry = Allergen.objects.get(name=allergen)
            notif.allergens.add(entry)
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
                'amount': notif.amount_of_food_left,
                'allergens': [x.name for x in notif.allergens.all()],
            },
            'userAgent': notif.host_user_agent,
            'ended': notif.ended
        }

    def to_internal_value(self, data):
        if 'netID' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a netID field"})
        if 'location' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a location field"})
        if 'event' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have an event field"})
        if 'duration' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a duration field"})
        if 'food' not in data or "served" not in data["food"] or "amount" \
            not in data["food"]:
            raise ValidationError({
                "Bad Request": "Post data must have a food field"})
        if 'bring_container' not in data:
            raise ValidationError({
                "Bad Request": "Post data must have a bring_container field"})
        if 'host' not in data or 'userAgent' not in data["host"]:
            raise ValidationError({
                "Bad Request": "Post data must have a host.userAgent field"})
        ret = {
            'location': data["location"],
            'event': data["event"],
            'food_served': data["food"]["served"],
            'amount_of_food_left': data["food"]["amount"],
            'bring_container': data["bring_container"],
            'allergens': None,
            'host_user_agent': data["host"]["userAgent"]
        }

        current_time = datetime.now().astimezone()
        end_time = current_time + timedelta(seconds=data["duration"])
        #import pdb; pdb.set_trace();
        ret["created_time"] = current_time
        ret["end_time"] = end_time

        if "allergens" in data["food"] and data["food"]["allergens"] != []:
            ret["allergens"] = data["food"]["allergens"]
        if ret["location"] == "" or ret["location"] == None:
            raise ValidationError({"location": "A location must be provided"})
        if ret["event"] == "" or ret["event"] == None:
            raise ValidationError({"event": "An event must be provided"})
        if ret["food_served"] == "" or ret["food_served"] == None:
            raise ValidationError(
                {"food_served": "At least one food served is required"})
        if ret["amount_of_food_left"] == "" or ret["amount_of_food_left"] == None:
            raise ValidationError(
                {"amount_of_food_left": "Food amounts must be specified"})
        if ret["host_user_agent"] == "" or ret["host_user_agent"] == None:
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


class SubscriptionSerializerList(serializers.ModelSerializer):
    sms_number = PhoneNumberField(allow_blank=True)

    class Meta:
        model = Subscription
        fields = ('id', 'netid', 'sms_number', 'number_verified', 'email',
                  'email_verified', 'notif_on')


class SubscriptionSerializer(serializers.ModelSerializer):
    sms_number = PhoneNumberField(allow_blank=True)

    class Meta:
        model = Subscription
        fields = ('id', 'netid', 'sms_number', 'email', 'notif_on')

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

        return ret

    def create(self, validated_data):
        sub, created = Subscription.objects.get_or_create(
            user=self.context.get('request').user)

        sub.email = validated_data["email"]
        sub.sms_number = validated_data["sms_number"]
        sub.notif_on = False

        sub.save()

        return sub
