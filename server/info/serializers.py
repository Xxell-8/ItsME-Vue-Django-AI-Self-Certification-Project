from .models import Link, Customer, IdCard
from rest_framework import serializers
from .utils.image import image_to_base64



class CustomerSerializer(serializers.ModelSerializer):
    id_card_image = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['link']
        extra_kwargs = {
            'img': {'write_only': True}
        }

    def get_id_card_image(self, obj):
        if obj.img:
            return image_to_base64(f'media/{obj.img.name}')
        return ''


class LinkListSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    complete_cnt = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ['partner', 'created_at']

    def get_total(self, obj):
        return obj.customers.count()

    def get_complete_cnt(self, obj):
        return obj.customers.filter(is_completed=True).count()


class LinkDetailSerializer(serializers.ModelSerializer):
    customers = CustomerSerializer(many=True)

    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ['partner', 'created_at']
    
    def create(self, validated_data):
        customers_data = validated_data.pop('customers')
        managers = validated_data.pop('managers')
        link = Link.objects.create(**validated_data)
        link.managers.set(managers)
        for customer_data in customers_data:
            Customer.objects.create(link=link, **customer_data)
        return link


class IdCardSerializer(serializers.ModelSerializer):
    id_card_image = serializers.SerializerMethodField()

    class Meta:
        model = IdCard
        fields = '__all__'
        read_only_fields = ['link']
        extra_kwargs = {
            'img': {'write_only': True}
        }

    def get_id_card_image(self, obj):
        return image_to_base64(f'media/{obj.img.name}')
