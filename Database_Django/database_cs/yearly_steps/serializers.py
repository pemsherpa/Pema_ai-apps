from rest_framework import serializers
from .models import ShoppingCartContent

class ShoppingCartContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartContent
        fields = '__all__'  