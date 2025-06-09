from rest_framework import serializers
from .models import Phones, PhoneVariant, Accessory, FlashDeal
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
            'id', 'sku', 'color', 'storage', 'price', 'sale_price', 
            'stock', 'image', 'is_active', 'is_new_arrival', 
            'is_best_seller', 'is_flash_deal', 'flash_deal_end',
            'name', 'brand', 'slug', 'image_url', 'description'
        ]
        read_only_fields = ['discount_percentage']
    
    def get_image_url(self, obj):
        if obj.image:
            return urljoin(settings.MEDIA_URL, obj.image.name)
        return None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.sale_price and instance.price:
            discount = ((instance.price - instance.sale_price) / instance.price) * 100
            data['discount_percentage'] = round(discount)
        else:
            data['discount_percentage'] = None
        return data    



class AccessorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
   
    class Meta:
        model = Accessory
        fields = [
            'id', 'name', 'slug', 'description', 'price', 
            'sale_price', 'stock', 'image', 'is_active',
            'is_new_arrival', 'is_best_seller', 'is_flash_deal', 
            'flash_deal_end', 'image_url', 'discount_percentage'
        ]

    def get_image_url(self, obj):
        if obj.image:
            return urljoin(settings.MEDIA_URL, obj.image.name)
        return None

    def get_discount_percentage(self, obj):
        if obj.sale_price and obj.price:
            return round(((obj.price - obj.sale_price) / obj.price) * 100)
        return None


class HomepageSectionSerializer(serializers.Serializer):
    phones = PhoneVariantSerializer(many=True, read_only=True)
    accessories = AccessorySerializer(many=True, read_only=True)


class FlashDealSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FlashDeal
        fields = [
            'id', 'name', 'slug', 'description', 'product_type', 
            'original_price', 'discount_percentage', 'sale_price',
            'start_date', 'end_date', 'is_active', 'stock',
            'image_url', 'reference_phone', 'reference_accessory'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
