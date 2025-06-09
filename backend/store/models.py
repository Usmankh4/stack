from enum import unique
import stripe
from unicodedata import category
import os
from django.db import models
from django.db.models.fields.files import ImageField
from django.utils.text import slugify
import uuid
from django.conf import settings
from django.core.exceptions import ValidationError


stripe.api_key = settings.STRIPE_SECRET_KEY

class Phones(models.Model):
    name=models.CharField(max_length=200)
    slug= models.CharField(max_length=255, unique=True, blank=True)
    brand = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    stripe_id = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand}-{self.name}")
            self.slug = base_slug
            n = 1
            while Phones.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{n}"
                n += 1
       
        if not self.stripe_id:
            try:
                stripe_product = stripe.Product.create(
                    name=self.name,
                    description=self.description or f"{self.brand} {self.name}",
                    metadata={
                        "brand": self.brand,
                        "product_id": str(self.id) if self.id else "pending",
                    }
                )
                self.stripe_id = stripe_product.id
            except Exception as e:
                print(f"Error creating Stripe product: {e}")
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.brand} {self.name}"
    
    class Meta:
        verbose_name_plural = "Phones"


class PhoneVariant(models.Model):
    phone = models.ForeignKey(Phones, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=50, unique=True, blank=True)
    color = models.CharField(max_length=100)
    storage = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    reservedStock = models.IntegerField(default=0)
    image = ImageField(upload_to='phones/', null=True, blank=True)
    stripe_price_id = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_flash_deal = models.BooleanField(default=False)
    flash_deal_end = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.sku:
            brand_code = self.phone.brand[:3].upper()
            model_code = self.phone.name[:4].upper()
            color_code = self.color[:3].upper()
            storage_code = self.storage.replace("GB", "").replace(" ", "")
            random_suffix = uuid.uuid4().hex[:6].upper()
            self.sku = f"{brand_code}-{model_code}-{color_code}-{storage_code}-{random_suffix}"
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if self.phone.stripe_id and (is_new or not self.stripe_price_id):
            try:
                price_in_cents = int(self.price * 100)
                stripe_price = stripe.Price.create(
                    product=self.phone.stripe_id,
                    unit_amount=price_in_cents,
                    currency='usd',
                    metadata={
                        'variant_id': str(self.id),
                        'sku': self.sku,
                        'color': self.color,
                        'storage': self.storage
                    }
                )
                self.__class__.objects.filter(id=self.id).update(stripe_price_id=stripe_price.id)
                self.stripe_price_id = stripe_price.id
            except Exception as e:
                print(f"Error creating Stripe price: {e}")

    def __str__(self):
        return f"{self.phone.name} - {self.color} - {self.storage}"

    class Meta:
        verbose_name_plural = "Phone Variants"


class Accessory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=255, unique=True, blank = True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    image = ImageField(upload_to='accessories/', null=True, blank=True)
    stripe_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_flash_deal = models.BooleanField(default=False)
    flash_deal_end = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            n = 1
            while Accessory.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{n}"
                n += 1

        if not self.stripe_id:
            try: 
                stripe_product = stripe.Product.create(
                    name=self.name,
                    description=self.description or self.name,
                    metadata={
                        "product_id": str(self.id) if self.id else "pending",
                        "product_type": "accessory"
                    }
                )
                self.stripe_id = stripe_product.id
                if not self.stripe_price_id:
                    price_in_cents = int(self.price*100)
                    stripe_price = stripe.Price.create(
                        product = self.stripe_id,
                        unit_amount=price_in_cents,
                        currency='cad',
                         metadata={
                            'accessory_id': str(self.id) if self.id else "pending"
                        }
                    )
                    self.stripe_price_id = stripe_price.id
            except Exception as e:
                print(f"Error creating Stripe product/price for accessory: {e}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Accessories"


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
    image = ImageField(upload_to='flash_deals/', null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    slug = models.CharField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    reference_phone = models.ForeignKey(PhoneVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='referenced_flash_deals')
    reference_accessory = models.ForeignKey(Accessory, on_delete=models.SET_NULL, null=True, blank=True, related_name='referenced_flash_deals')
    
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
        
        if not self.sale_price:
            discount = (self.discount_percentage / 100) * self.original_price
            self.sale_price = self.original_price - discount
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
