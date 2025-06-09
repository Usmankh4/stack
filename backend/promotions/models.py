from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from store.models import PhoneVariant, Accessory
from .utils import calculate_sale_price, calculate_discount_percentage

class FlashDeal(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('accessory', 'Accessory'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='flash_deals/', null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    slug = models.CharField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    reference_phone = models.ForeignKey(
        'store.PhoneVariant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='promotion_flash_deals'
    )
    reference_accessory = models.ForeignKey(
        'store.Accessory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='promotion_flash_deals'
    )
    
    class Meta:
        verbose_name_plural = "Flash Deals"
    
    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")
        
        # Only validate that a product can't reference both phone and accessory
        if self.reference_phone and self.reference_accessory:
            raise ValidationError("A flash deal can only reference either a phone variant or an accessory, not both.")
        
        # No longer require references based on product_type
        # References are now completely optional
    
    def update_prices(self, update_type='discount_to_sale'):
        """Update either sale price or discount percentage based on the other value
        
        Args:
            update_type (str): Either 'discount_to_sale' to calculate sale price from discount percentage,
                              or 'sale_to_discount' to calculate discount percentage from sale price
        """
        if update_type == 'discount_to_sale':
            self.sale_price = calculate_sale_price(self.original_price, self.discount_percentage)
        elif update_type == 'sale_to_discount':
            self.discount_percentage = calculate_discount_percentage(self.original_price, self.sale_price)
    
    def calculate_discount_from_prices(self):
        """
        Calculate and set the discount percentage based on original price and sale price.
        This is useful when you know both prices and want to determine the discount.
        """
        if self.original_price and self.sale_price:
            self.discount_percentage = calculate_discount_percentage(self.original_price, self.sale_price)
            return self.discount_percentage
        return None
    
    def calculate_sale_from_discount(self):
        """
        Calculate and set the sale price based on original price and discount percentage.
        This is useful when you know the original price and discount but need the final price.
        """
        if self.original_price and self.discount_percentage:
            self.sale_price = calculate_sale_price(self.original_price, self.discount_percentage)
            return self.sale_price
        return None
    
    def save(self, *args, **kwargs):
        self.clean()
        
        # If both original price and sale price are provided but no discount percentage,
        # calculate the discount percentage automatically
        if self.original_price and self.sale_price and not self.discount_percentage:
            self.calculate_discount_from_prices()
        
        # If original price and discount percentage are provided but no sale price,
        # calculate the sale price automatically
        elif self.original_price and self.discount_percentage and not self.sale_price:
            self.calculate_sale_from_discount()
        
        # Generate slug if not provided
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            n = 1
            while FlashDeal.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{n}"
                n += 1
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.discount_percentage}% off)"
