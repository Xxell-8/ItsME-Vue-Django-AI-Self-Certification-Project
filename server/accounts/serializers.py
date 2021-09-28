from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from .models import Partner, User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.registration.serializers import RegisterSerializer



# 커스텀 회원가입 serializer
# custom field 저장 안되는 문제 해결 : https://stackoverflow.com/questions/37841612/django-rest-auth-custom-registration-fails-to-save-extra-fields
class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = None
    last_name = None
    fullname = serializers.CharField()
    name = serializers.CharField()
    code = serializers.CharField()
    phone = serializers.CharField()
    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'fullname': self.validated_data.get('fullname', ''),
            'email': self.validated_data.get('email', ''),
            'code': self.validated_data.get('code', ''),
            'name': self.validated_data.get('name', ''),
            'phone': self.validated_data.get('phone', ''),
        }
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.fullname = self.cleaned_data.get('fullname')
        user.code = self.cleaned_data.get('code')
        user.name = self.cleaned_data.get('name')
        user.phone = self.cleaned_data.get('phone')
        user.save()
        return user

class PartnerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Partner
        fields = ['id', 'code', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'auth', 'fullname', 'code', 'name', 'email', 'phone']


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone']

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class PartnerRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['auth', 'name', 'code']
    
    def validate_email(self, value):
        user = self.context['request'].user

        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({'email': 'This email is already in use.'})
        return value

    def validate_code(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(code=value).exists():
            raise serializers.ValidationError({'code': 'This code is already in use.'})
        return value

    def update(self, instance, validated_data):
        if instance.auth:
            instance.auth = 0
            partner = Partner.objects.get(code=instance.code)
            partner.delete()
        else:
            instance.auth = 1
            Partner.objects.create(
                name = instance.name,
                code = instance.code
            )

        instance.save()

        return instance

class UserApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['approval']

    def update(self, instance, validated_data):
        if instance.approval:
            instance.approval = 0
        else:
            instance.approval = 1

        instance.save()

        return instance

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'auth', 'fullname', 'name', 'email', 'phone']