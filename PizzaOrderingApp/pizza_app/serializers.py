from rest_framework import serializers
from rest_framework.views import APIView
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    # role = serializers.CharField()


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password', 'role']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

