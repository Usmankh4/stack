from rest_framework import serializers
from .models import Phones, PhoneVariant, Accessory
from urllib.parse import urljoin
from django.conf import settings

class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phones
        fields = ['id', 'name', 'slug', 'brand', 'description']


class PhoneVariantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='phone.name', read_only=True)
    brand = serializers.CharField(source='phone.brand', read_only=True)
    slug = serializers.CharField(source='phone.slug', read_only=True)
    image_url = serializers.SerializerMethodField()
    description = serializers.CharField(source='phone.description', read_only=True)
    
    class Meta:
        model = PhoneVariant
        fields = [
            'id', 'sku', 'color', 'storage', 'price',
            'stock', 'image', 'is_active', 'is_new_arrival', 
            'is_best_seller', 'name', 'brand', 'slug', 'image_url', 'description'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            return urljoin(settings.MEDIA_URL, obj.image.name)
        return None    



class AccessorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
   
    class Meta:
        model = Accessory
        fields = [
            'id', 'name', 'slug', 'description', 'price', 
            'stock', 'image', 'is_active',
            'is_new_arrival', 'is_best_seller', 'image_url'
        ]

    def get_image_url(self, obj):
        if obj.image:
            return urljoin(settings.MEDIA_URL, obj.image.name)
        return None


class HomepageSectionSerializer(serializers.Serializer):
    phones = PhoneVariantSerializer(many=True, read_only=True)
    accessories = AccessorySerializer(many=True, read_only=True)


# FlashDealSerializer has been moved to the promotions app
