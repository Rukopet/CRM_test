from django.db import models


class ClientModel(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.SlugField(max_length=30)
    client_telegram_user_id = models.CharField(max_length=10)
    client_date_registration = models.DateTimeField(auto_now_add=True)


class BidModel(models.Model):

    enum_status = (
        (1, 'open'),
        (2, 'in work'),
        (3, 'finished'),
    )

    enum_type_bid = (
        (1, 'fix'),
        (2, 'consultation'),
        (3, 'service')
    )

    type_bid = models.IntegerField(choices=enum_type_bid)
    creator = models.ManyToManyField('ClientModel', related_name="bids", blank=True)
    staff_id = models.IntegerField(blank=True, null=True)
    text_bid = models.CharField(max_length=400)
    title = models.CharField(max_length=100, db_index=True, default="Bid")
    status = models.IntegerField(choices=enum_status, default=1)
    date_create = models.DateField(auto_now_add=True)
    notifications = models.BooleanField(default=False)

class StaffModel(models.Model):
    a = 1