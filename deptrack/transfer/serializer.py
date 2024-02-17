from rest_framework import serializers
from .models import Transfer,TransferDetails



class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"

class TransferDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferDetails
        fields = "__all__"