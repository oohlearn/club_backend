from rest_framework import serializers
from .models import Contact, Customer


# Contact
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


# 購買者
class CustomerSerialize(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'