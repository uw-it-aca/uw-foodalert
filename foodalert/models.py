from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Notification(models.Model):
    location = models.CharField(max_length=100, blank=False)
    event = models.CharField(max_length=40, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    food_served = models.CharField(max_length=100, blank=False)
    amount_of_food_left = models.CharField(max_length=100, blank=False)
    bring_container = models.BooleanField(default=False)
    safe_foods = models.ManyToManyField(
        'SafeFood', related_name='safe_foods', blank=True)
    allergens = models.ManyToManyField(
        'Allergen', related_name='allergens', blank=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    host_user_agent = models.TextField(blank=False)
    ended = models.BooleanField(default=False)


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    email_verified = models.BooleanField(default=False)
    sms_number = PhoneNumberField(blank=True)
    number_verified = models.BooleanField(default=False)
    notif_on = models.BooleanField(default=False)

    @property
    def netid(self):
        return self.user.email


class Update(models.Model):
    text = models.CharField(max_length=100, blank=False)
    parent_notification = models.ForeignKey('Notification',
                                            blank=False,
                                            on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class SafeFood(models.Model):
    name = models.CharField(max_length=30)


class Allergen(models.Model):
    name = models.CharField(max_length=30, unique=True)
