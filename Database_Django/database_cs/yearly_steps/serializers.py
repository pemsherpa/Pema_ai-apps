from rest_framework import serializers
from .models import *
from .views_query import *

class ShoppingCartContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartContent
        fields = '__all__'  