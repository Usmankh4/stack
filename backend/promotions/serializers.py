from rest_framework import serializers
from .models import FlashDeal
from django.conf import settings

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
