from django.db.models import Q
from ..models import PhoneVariant, Accessory, Phones

class ProductService:
    @staticmethod
    def get_new_arrivals(limit=8):
        """
        Get new arrival products (both phones and accessories)
        """
        phone_new_arrivals = PhoneVariant.objects.filter(
            is_new_arrival=True, 
            is_active=True
        ).select_related('phone')[:limit]
        
        accessory_new_arrivals = Accessory.objects.filter(
            is_new_arrival=True, 
            is_active=True
        )[:limit]
        
        return {
            'phones': phone_new_arrivals,
            'accessories': accessory_new_arrivals
        }
    
    @staticmethod
    def get_best_sellers(limit=8):
        """
        Get best seller products (both phones and accessories)
        """
        phone_best_sellers = PhoneVariant.objects.filter(
            is_best_seller=True, 
            is_active=True
        ).select_related('phone')[:limit]
        
        accessory_best_sellers = Accessory.objects.filter(
            is_best_seller=True, 
            is_active=True
        )[:limit]
        
        return {
            'phones': phone_best_sellers,
            'accessories': accessory_best_sellers
        }
    
    @staticmethod
    def get_phone_by_slug(slug):
        """
        Get a phone and its variants by slug
        """
        try:
            phone = Phones.objects.get(slug=slug)
            variants = PhoneVariant.objects.filter(phone=phone, is_active=True)
            return phone, variants
        except Phones.DoesNotExist:
            return None, None
    
    @staticmethod
    def get_accessory_by_slug(slug):
        """
        Get an accessory by slug
        """
        try:
            return Accessory.objects.get(slug=slug, is_active=True)
        except Accessory.DoesNotExist:
            return None
    
    @staticmethod
    def get_related_products(product, limit=4):
        """
        Get related products based on product type
        """
        if isinstance(product, Phones):
            # Get phones of the same brand
            return PhoneVariant.objects.filter(
                Q(phone__brand=product.brand) & ~Q(phone=product),
                is_active=True
            ).select_related('phone')[:limit]
        elif isinstance(product, Accessory):
            # Get other accessories
            return Accessory.objects.filter(
                ~Q(id=product.id),
                is_active=True
            )[:limit]
        return []
