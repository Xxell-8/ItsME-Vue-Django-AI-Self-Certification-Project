from .models import Link, Customer
from rest_framework import serializers



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['link']


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

class IdCardSerializer(serializers.Serializer):
    image = serializers.ImageField()
