from .models import ClientModel, BidModel, StaffModel
from rest_framework import serializers

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


class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = ("__all__")


class StaffModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffModel
        fields = ("__all__")


class BidModelSerializer(serializers.ModelSerializer):
    creator = ClientModelSerializer(many=True)
    status = serializers.CharField(source='get_status_display')
    type_bid = serializers.CharField(source='get_type_bid_display')
    staff_id = StaffModelSerializer(many=True)

    class Meta:
        model = BidModel
        fields = ("__all__")


