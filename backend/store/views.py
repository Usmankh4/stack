from django.utils import timezone
from django.db.models import Q
from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Phones, PhoneVariant, Accessory
from .serializers import (
    PhoneSerializer, 
    PhoneVariantSerializer, 
    AccessorySerializer
)

class ProductPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 20

class HomepageAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        cache_key = 'homepage_data'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
            
        now = timezone.now()
        
        phone_flash_deals = PhoneVariant.objects.filter(
            is_flash_deal=True, 
            is_active=True,
            flash_deal_end__gt=now
        ).select_related('phone')[:8]
        
        accessory_flash_deals = Accessory.objects.filter(
            is_flash_deal=True, 
            is_active=True,
            flash_deal_end__gt=now
        )[:8]
        
        phone_new_arrivals = PhoneVariant.objects.filter(
            is_new_arrival=True, 
            is_active=True
        ).select_related('phone')[:8]
        
        accessory_new_arrivals = Accessory.objects.filter(
            is_new_arrival=True, 
            is_active=True
        )[:8]
        
        phone_best_sellers = PhoneVariant.objects.filter(
            is_best_seller=True, 
            is_active=True
        ).select_related('phone')[:8]
        
        accessory_best_sellers = Accessory.objects.filter(
            is_best_seller=True, 
            is_active=True
        )[:8]
        response_data = {
            'flash_deals': PhoneVariantSerializer(
                phone_flash_deals, 
                many=True,
                context={'request': request}
            ).data + AccessorySerializer(
                accessory_flash_deals,
                many=True,
                context={'request': request}
            ).data,
            
            'new_arrivals': PhoneVariantSerializer(
                phone_new_arrivals,
                many=True,
                context={'request': request}
            ).data + AccessorySerializer(
                accessory_new_arrivals,
                many=True,
                context={'request': request}
            ).data,
            
            'best_sellers': PhoneVariantSerializer(
                phone_best_sellers,
                many=True,
                context={'request': request}
            ).data + AccessorySerializer(
                accessory_best_sellers,
                many=True,
                context={'request': request}
            ).data
        }
        
        cache.set(cache_key, response_data, 60 * 15)
        return Response(response_data)

class FlashDealsAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    
    def get(self, request, format=None):
        now = timezone.now()
        
        phone_flash_deals = PhoneVariant.objects.filter(
            is_flash_deal=True, 
            is_active=True,
            flash_deal_end__gt=now
        ).select_related('phone')
        
        accessory_flash_deals = Accessory.objects.filter(
            is_flash_deal=True, 
            is_active=True,
            flash_deal_end__gt=now
        )
       
        end_time = None
        if phone_flash_deals.exists():
            end_time = phone_flash_deals.first().flash_deal_end
        elif accessory_flash_deals.exists():
            end_time = accessory_flash_deals.first().flash_deal_end
        
        response_data = {
            'products': PhoneVariantSerializer(
                phone_flash_deals,
                many=True,
                context={'request': request}
            ).data + AccessorySerializer(
                accessory_flash_deals,
                many=True,
                context={'request': request}
            ).data,
            'end_time': end_time
        }
        
        return Response(response_data)

class NewArrivalsAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    
    def get(self, request, format=None):
        phone_new_arrivals = PhoneVariant.objects.filter(
            is_new_arrival=True, 
            is_active=True
        ).select_related('phone')
        
        accessory_new_arrivals = Accessory.objects.filter(
            is_new_arrival=True, 
            is_active=True
        )
        
        response_data = {
            'products': PhoneVariantSerializer(
                phone_new_arrivals,
                many=True,
                context={'request': request}
            ).data + AccessorySerializer(
                accessory_new_arrivals,
                many=True,
                context={'request': request}
            ).data
        }
        
        return Response(response_data)

class BestSellersAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    
    def get(self, request, format=None):
        phone_best_sellers = PhoneVariant.objects.filter(
            is_best_seller=True, 
            is_active=True
        ).select_related('phone')
        
        accessory_best_sellers = Accessory.objects.filter(
            is_best_seller=True, 
            is_active=True
        )
        
        response_data = {
            'products': PhoneVariantSerializer(
                phone_best_sellers,
                many=True,
                context={'request': request}
            ).data + AccessorySerializer(
                accessory_best_sellers,
                many=True,
                context={'request': request}
            ).data
        }
        
        return Response(response_data)

class PhoneVariantDetailAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, slug, format=None):
        try:
            phone = Phones.objects.get(slug=slug)
            variants = PhoneVariant.objects.filter(phone=phone, is_active=True)
            
            if not variants.exists():
                return Response(
                    {"error": "No active variants found for this phone"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            related_phones = PhoneVariant.objects.filter(
                Q(phone__brand=phone.brand) & ~Q(phone=phone),
                is_active=True
            ).select_related('phone')[:4]
            
            response_data = {
                'phone': PhoneSerializer(phone, context={'request': request}).data,
                'variants': PhoneVariantSerializer(
                    variants,
                    many=True,
                    context={'request': request}
                ).data,
                'related_products': PhoneVariantSerializer(
                    related_phones,
                    many=True,
                    context={'request': request}
                ).data
            }
            
            return Response(response_data)
            
        except Phones.DoesNotExist:
            return Response(
                {"error": "Phone not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class AccessoryDetailAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, slug, format=None):
        try:
            accessory = Accessory.objects.get(slug=slug, is_active=True)
            related_accessories = Accessory.objects.filter(
                ~Q(id=accessory.id),
                is_active=True
            )[:4]
            
            response_data = {
                'accessory': AccessorySerializer(
                    accessory,
                    context={'request': request}
                ).data,
                'related_products': AccessorySerializer(
                    related_accessories,
                    many=True,
                    context={'request': request}
                ).data
            }
            
            return Response(response_data)
        except Accessory.DoesNotExist:
            return Response(
                {"error": "Accessory not found"},
                status=status.HTTP_404_NOT_FOUND
            )