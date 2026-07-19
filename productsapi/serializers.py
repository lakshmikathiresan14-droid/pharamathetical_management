from rest_framework import serializers
from store .models import Medicine
from django.contrib.auth.models import User

class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def validate(self, data):
        # Check if the two passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Remove password2 from the validated data
        validated_data.pop('password2')
        # Create a new user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        return user



class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ('id',  'name', 'description','price', 'expiry_date')
        

    def create(self, validated_data):
        return super().create(validated_data)