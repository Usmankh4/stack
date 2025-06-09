from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from .services.flash_deal_service import FlashDealService
from .serializers import FlashDealSerializer
from store.services.product_service import ProductService
from store.serializers import PhoneVariantSerializer, AccessorySerializer

class FlashDealsAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        """
        Get all active flash deals
        """
        cache_key = 'flash_deals'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        flash_deals = FlashDealService.get_active_flash_deals()
        serialized_data = FlashDealSerializer(
            flash_deals, 
            many=True,
            context={'request': request}
        ).data
        
        # Cache for 15 minutes
        cache.set(cache_key, serialized_data, 60 * 15)
        return Response(serialized_data)

class HomepageAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        """
        Get data for the homepage including flash deals, new arrivals, and best sellers
        """
        cache_key = 'homepage_data'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Get flash deals
        flash_deals = FlashDealService.get_active_flash_deals(limit=8)
        
        # Get new arrivals
        new_arrivals = ProductService.get_new_arrivals(limit=8)
        
        # Get best sellers
        best_sellers = ProductService.get_best_sellers(limit=8)
        
        response_data = {
            'flash_deals': FlashDealSerializer(
                flash_deals, 
                many=True,
                context={'request': request}
            ).data,
            'new_arrivals': {
                'phones': PhoneVariantSerializer(
                    new_arrivals['phones'],
                    many=True,
                    context={'request': request}
                ).data,
                'accessories': AccessorySerializer(
                    new_arrivals['accessories'],
                    many=True,
                    context={'request': request}
                ).data
            },
            'best_sellers': {
                'phones': PhoneVariantSerializer(
                    best_sellers['phones'],
                    many=True,
                    context={'request': request}
                ).data,
                'accessories': AccessorySerializer(
                    best_sellers['accessories'],
                    many=True,
                    context={'request': request}
                ).data
            }
        }
        
        # Cache for 15 minutes
        cache.set(cache_key, response_data, 60 * 15)
        return Response(response_data)
