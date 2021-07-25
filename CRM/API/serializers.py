from .models import ClientModel, BidModel
from rest_framework import serializers


class ClientModelSerializer(serializers.ModelSerializer):
    class Meta

class BidModelSerializer(serializers.ModelSerializer):

    client_id
    class Meta:
        model = BidModel
        fields = ("pk", "type_bid", "client_id", "staff_id", "text_bid", "title", "status", "date_create",
                  "notifications")
