from .models import Partner, User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# 참고 URL : https://velog.io/@lemontech119/DRF%EB%A1%9C-%EC%84%9C%EB%B2%84-%EA%B0%9C%EB%B0%9C1-%ED%9A%8C%EC%9B%90%EA%B8%B0%EB%8A%A5
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is None:
            return {
                'username': 'None'
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exists.'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }