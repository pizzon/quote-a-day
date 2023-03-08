from .models import Quotes, PhoneNumber, SecondaryEmail
from rest_framework import serializers
from django.contrib.auth.models import User


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotes
        fields = ('quote', 'author', 'date')


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField('get_phone_number')
    
    secondary_email = serializers.SerializerMethodField('get_secondary_email')

    def get_phone_number(self, user):
        numbers = []
        qs = PhoneNumber.objects.filter(user=user.id)
        for q in qs:
            numbers.append(q.phone_number)
        return numbers
    
    def get_secondary_email(self, user):
        emails = []
        qs = SecondaryEmail.objects.filter(user=user.id)
        for q in qs:
            emails.append(q.secondary_email)
        return emails

    class Meta:
        model = User
        fields = ('id','username','email','phone_number', 'secondary_email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        return user

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        exclude = ('user','id')

class SecondaryEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryEmail
        exclude = ('user','id')