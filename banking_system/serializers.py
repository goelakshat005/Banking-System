from rest_framework import serializers
from .models import User, Transactions 

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        mdoel = User
        fields = "__all__"

class Transactions_Serializer(serializers.ModelSerializer):
    class Meta:
        mdoel = Transactions
        fields = "__all__"