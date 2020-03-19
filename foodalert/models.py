from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Notification(models.Model):
    location = models.CharField(max_length=200, blank=False)
    event = models.CharField(max_length=40, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    food_served = models.CharField(max_length=200, blank=False)
    food_qualifications = models.ManyToManyField(
        'FoodQualification', blank=False)
    bring_container = models.BooleanField(default=False)
    allergens = models.ManyToManyField(
        'Allergen', related_name='allergens', blank=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    host_user_agent = models.TextField(blank=False)
    ended = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_time',)


class FoodQualification(models.Model):
    internalName = models.CharField(max_length=20, blank=False, unique=True)
    externalName = models.CharField(max_length=50, blank=False, unique=True)


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    email_verified = models.BooleanField(default=True)
    send_email = models.BooleanField(default=False)
    sms_number = PhoneNumberField(blank=True)
    number_verified = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    twilio_stop = models.BooleanField(default=False)

    @property
    def netid(self):
        return self.user.username


class Update(models.Model):
    text = models.CharField(max_length=150, blank=False)
    parent_notification = models.ForeignKey('Notification',
                                            blank=False,
                                            on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_time',)


class Allergen(models.Model):
    name = models.CharField(max_length=30, unique=True)
