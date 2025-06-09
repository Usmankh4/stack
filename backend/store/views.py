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
from .services.product_service import ProductService

class ProductPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 20

class NewArrivalsAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    
    def get(self, request, format=None):
        cache_key = 'new_arrivals'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
            
        new_arrivals = ProductService.get_new_arrivals()
        
        response_data = {
            'products': PhoneVariantSerializer(
                new_arrivals['phones'],
                many=True,
                context={'request': request}
            ).data + AccessorySerializer(
                new_arrivals['accessories'],
                many=True,
                context={'request': request}
            ).data
        }
        
        # Cache for 15 minutes
        cache.set(cache_key, response_data, 60 * 15)
        return Response(response_data)

class BestSellersAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    
    def get(self, request, format=None):
        cache_key = 'best_sellers'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
            
        best_sellers = ProductService.get_best_sellers()
        
        response_data = {
            'products': PhoneVariantSerializer(
                best_sellers['phones'],
                many=True,
                context={'request': request}
            ).data + AccessorySerializer(
                best_sellers['accessories'],
                many=True,
                context={'request': request}
            ).data
        }
        
        # Cache for 15 minutes
        cache.set(cache_key, response_data, 60 * 15)
        
        return Response(response_data)

class PhoneVariantDetailAPIView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, slug, format=None):
        try:
            cache_key = f'phone_detail_{slug}'
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
                
            product_data = ProductService.get_phone_details_by_slug(slug)
            if not product_data:
                return Response(
                    {"error": "Phone not found or has no active variants"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            response_data = {
                'phone': PhoneSerializer(product_data['phone'], context={'request': request}).data,
                'variants': PhoneVariantSerializer(
                    product_data['variants'],
                    many=True,
                    context={'request': request}
                ).data,
                'related_products': PhoneVariantSerializer(
                    product_data['related_products'],
                    many=True,
                    context={'request': request}
                ).data
            }
            
            # Cache for 15 minutes
            cache.set(cache_key, response_data, 60 * 15)
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

class AccessoryDetailAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, slug, format=None):
        try:
            cache_key = f'accessory_detail_{slug}'
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
                
            product_data = ProductService.get_accessory_details_by_slug(slug)
            if not product_data:
                return Response(
                    {"error": "Accessory not found or not active"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            response_data = {
                'accessory': AccessorySerializer(
                    product_data['accessory'],
                    context={'request': request}
                ).data,
                'related_products': AccessorySerializer(
                    product_data['related_products'],
                    many=True,
                    context={'request': request}
                ).data
            }
            
            # Cache for 15 minutes
            cache.set(cache_key, response_data, 60 * 15)
            return Response(response_data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )