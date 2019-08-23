from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string
# Create your models here.


class Notification(models.Model):
    location = models.CharField(max_length=100, blank=False)
    event = models.CharField(max_length=40, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    food_served = models.CharField(max_length=100, blank=False)
    amount_of_food_left = models.CharField(max_length=100, blank=False)
    bring_container = models.BooleanField(default=False)
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
    # make sure it is not writable
    email_code = models.CharField(max_length=20, blank=True)

    __original_email = None

    @property
    def netid(self):
        return self.user.username

    def __init__(self, *args, **kwargs):
        super(Subscription, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.email != self.__original_email and self.email != "":
            #create random email code
            unique_code = get_random_string(length=20)
            self.email_code = unique_code
        super(Subscription, self).save()
        self.__original_email = self.email


class Update(models.Model):
    text = models.CharField(max_length=100, blank=False)
    parent_notification = models.ForeignKey('Notification',
                                            blank=False,
                                            on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Allergen(models.Model):
    name = models.CharField(max_length=30, unique=True)
