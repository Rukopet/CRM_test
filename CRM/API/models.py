from django.db import models


class BidModel(models.Model):

    enum_status = [
        (1, 'open'),
        (2, 'in work'),
        (3, 'finished'),
    ]

    enum_type_bid = [
        (1, 'fix'),
        (2, 'consultation'),
        (3, 'service')
    ]

    type_bid = models.IntegerField(choices=enum_type_bid)
    client_id = models.IntegerField()
    staff_id = models.IntegerField(blank=True)
    text_bid = models.CharField(max_length=400, db_index=True)
    title = models.CharField(max_length=100, db_index=True)
    status = models.IntegerField(choices=enum_status)
    date_create = models.DateField(auto_now_add=True)
    notifications = models.BooleanField(default=False)

    # def __str__(self):
    #     return f'{self.type_bid} {self.text_bid} {self.status}'


class ClientModel(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.SlugField(max_length=30)
    client_telegram_user_id = models.CharField(max_length=10)
    client_date_registration = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f'{self.client_id} | {self.client_name} | {self.client_telegram_user_id} | ' \
    #            f'{self.client_date_registration}'
