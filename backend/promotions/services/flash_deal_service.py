from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from ..models import FlashDeal
from ..utils import calculate_sale_price, calculate_discount_percentage, apply_discount

class FlashDealService:
    @staticmethod
    def get_active_flash_deals(limit=None):
        """
        Get all active flash deals that are currently running
        """
        now = timezone.now()
        query = FlashDeal.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gt=now
        )
        
        if limit:
            return query[:limit]
        return query
    
    @staticmethod
    def get_flash_deal_by_slug(slug):
        """
        Get a specific flash deal by its slug
        """
        try:
            return FlashDeal.objects.get(slug=slug, is_active=True)
        except FlashDeal.DoesNotExist:
            return None
    
    @staticmethod
    def get_upcoming_flash_deals(limit=None):
        """
        Get flash deals that haven't started yet
        """
        now = timezone.now()
        query = FlashDeal.objects.filter(
            is_active=True,
            start_date__gt=now
        ).order_by('start_date')
        
        if limit:
            return query[:limit]
        return query
    
    @staticmethod
    def create_flash_deal_from_product(product, discount_percentage, start_date, end_date, name=None, description=None):
        """
        Create a flash deal from an existing product with automatic price calculation
        
        Args:
            product: Either a PhoneVariant or Accessory instance
            discount_percentage (Decimal): The discount percentage to apply
            start_date (datetime): When the flash deal starts
            end_date (datetime): When the flash deal ends
            name (str, optional): Custom name for the flash deal. If None, uses product name
            description (str, optional): Custom description. If None, uses product description
            
        Returns:
            FlashDeal: The created flash deal instance
        """
        from store.models import PhoneVariant, Accessory
        
        with transaction.atomic():
            # Determine product type and set reference
            if isinstance(product, PhoneVariant):
                product_type = 'phone'
                reference_phone = product
                reference_accessory = None
                original_price = product.price
                product_name = f"{product.phone.brand} {product.phone.name} {product.color} {product.storage}"
                product_description = product.phone.description
                product_image = product.image
            elif isinstance(product, Accessory):
                product_type = 'accessory'
                reference_phone = None
                reference_accessory = product
                original_price = product.price
                product_name = product.name
                product_description = product.description
                product_image = product.image
            else:
                raise ValueError("Product must be either a PhoneVariant or Accessory instance")
            
            # Calculate sale price
            sale_price = calculate_sale_price(original_price, discount_percentage)
            
            # Create flash deal
            flash_deal = FlashDeal(
                name=name or f"{product_name} Flash Deal",
                description=description or product_description,
                product_type=product_type,
                original_price=original_price,
                discount_percentage=discount_percentage,
                sale_price=sale_price,
                image=product_image,
                start_date=start_date,
                end_date=end_date,
                is_active=True,
                stock=product.stock,
                reference_phone=reference_phone,
                reference_accessory=reference_accessory
            )
            
            flash_deal.save()
            return flash_deal
    
    @staticmethod
    def create_flash_deal_with_custom_price(product, sale_price, start_date, end_date, name=None, description=None):
        """
        Create a flash deal from an existing product with a custom sale price
        
        Args:
            product: Either a PhoneVariant or Accessory instance
            sale_price (Decimal): The custom sale price
            start_date (datetime): When the flash deal starts
            end_date (datetime): When the flash deal ends
            name (str, optional): Custom name for the flash deal. If None, uses product name
            description (str, optional): Custom description. If None, uses product description
            
        Returns:
            FlashDeal: The created flash deal instance
        """
        from store.models import PhoneVariant, Accessory
        
        with transaction.atomic():
            # Determine product type and set reference
            if isinstance(product, PhoneVariant):
                product_type = 'phone'
                reference_phone = product
                reference_accessory = None
                original_price = product.price
                product_name = f"{product.phone.brand} {product.phone.name} {product.color} {product.storage}"
                product_description = product.phone.description
                product_image = product.image
            elif isinstance(product, Accessory):
                product_type = 'accessory'
                reference_phone = None
                reference_accessory = product
                original_price = product.price
                product_name = product.name
                product_description = product.description
                product_image = product.image
            else:
                raise ValueError("Product must be either a PhoneVariant or Accessory instance")
            
            # Calculate discount percentage
            discount_percentage = calculate_discount_percentage(original_price, sale_price)
            
            # Create flash deal
            flash_deal = FlashDeal(
                name=name or f"{product_name} Flash Deal",
                description=description or product_description,
                product_type=product_type,
                original_price=original_price,
                discount_percentage=discount_percentage,
                sale_price=sale_price,
                image=product_image,
                start_date=start_date,
                end_date=end_date,
                is_active=True,
                stock=product.stock,
                reference_phone=reference_phone,
                reference_accessory=reference_accessory
            )
            
            flash_deal.save()
            return flash_deal
    
    @staticmethod
    def batch_create_flash_deals(products, discount_percentage, start_date, end_date):
        """
        Create multiple flash deals with the same discount percentage
        
        Args:
            products: List of PhoneVariant or Accessory instances
            discount_percentage (Decimal): The discount percentage to apply to all products
            start_date (datetime): When the flash deals start
            end_date (datetime): When the flash deals end
            
        Returns:
            list: The created flash deal instances
        """
        created_deals = []
        for product in products:
            deal = FlashDealService.create_flash_deal_from_product(
                product=product,
                discount_percentage=discount_percentage,
                start_date=start_date,
                end_date=end_date
            )
            created_deals.append(deal)
        return created_deals
