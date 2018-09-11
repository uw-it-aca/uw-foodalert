from rest_framework import serializers
from foodalert.models import Notification, Update, SafeFood, Allergen

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('location', 'location_details', 'event', 'created_time',
                  'end_time', 'food_served', 'amount_of_food_left', 'host',
                  'bring_container', 'safe_foods', 'allergens',
                  'host_permit_number', 'host_user_agent')

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
