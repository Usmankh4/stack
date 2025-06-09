from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from store.models import PhoneVariant, Accessory

class FlashDeal(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('accessory', 'Accessory'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='flash_deals/', null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    slug = models.CharField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reference fields to original products (optional)
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
        
        if self.reference_phone and self.reference_accessory:
            raise ValidationError("A flash deal can only reference either a phone variant or an accessory, not both.")
        
        if self.product_type == 'phone' and not self.reference_phone:
            raise ValidationError("For phone product type, a reference phone must be selected.")
        
        if self.product_type == 'accessory' and not self.reference_accessory:
            raise ValidationError("For accessory product type, a reference accessory must be selected.")
    
    def save(self, *args, **kwargs):
        self.clean()
        
        # Calculate sale price if not provided
        if not self.sale_price:
            discount = (self.discount_percentage / 100) * self.original_price
            self.sale_price = self.original_price - discount
        
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
