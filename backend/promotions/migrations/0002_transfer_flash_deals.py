from django.db import migrations
from django.utils import timezone
from django.utils.text import slugify

def transfer_flash_deals(apps, schema_editor):
    """
    Transfer existing flash deals from PhoneVariant and Accessory models to the new FlashDeal model
    """
    PhoneVariant = apps.get_model('store', 'PhoneVariant')
    Accessory = apps.get_model('store', 'Accessory')
    FlashDeal = apps.get_model('promotions', 'FlashDeal')
    
    # Transfer flash deals from PhoneVariant
    phone_flash_deals = PhoneVariant.objects.filter(is_flash_deal=True)
    for phone in phone_flash_deals:
        # Skip if end date is in the past
        if phone.flash_deal_end and phone.flash_deal_end < timezone.now():
            continue
            
        # Calculate discount percentage
        discount_percentage = 0
        if phone.sale_price and phone.price > 0:
            discount_percentage = round((1 - (phone.sale_price / phone.price)) * 100, 2)
        
        # Create slug
        base_slug = f"{slugify(phone.phone.name)}-{slugify(phone.color)}-{slugify(phone.storage)}-flash-deal"
        slug = base_slug
        n = 1
        while FlashDeal.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{n}"
            n += 1
        
        # Create flash deal
        FlashDeal.objects.create(
            name=f"{phone.phone.name} {phone.color} {phone.storage}",
            description=phone.phone.description,
            product_type='phone',
            original_price=phone.price,
            discount_percentage=discount_percentage,
            sale_price=phone.sale_price,
            image=phone.image,
            start_date=timezone.now() - timezone.timedelta(days=1),  # Started yesterday
            end_date=phone.flash_deal_end or (timezone.now() + timezone.timedelta(days=7)),  # Default 7 days
            is_active=True,
            stock=phone.stock,
            slug=slug,
            reference_phone=phone
        )
    
    # Transfer flash deals from Accessory
    accessory_flash_deals = Accessory.objects.filter(is_flash_deal=True)
    for accessory in accessory_flash_deals:
        # Skip if end date is in the past
        if accessory.flash_deal_end and accessory.flash_deal_end < timezone.now():
            continue
            
        # Calculate discount percentage
        discount_percentage = 0
        if accessory.sale_price and accessory.price > 0:
            discount_percentage = round((1 - (accessory.sale_price / accessory.price)) * 100, 2)
        
        # Create slug
        base_slug = f"{slugify(accessory.name)}-flash-deal"
        slug = base_slug
        n = 1
        while FlashDeal.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{n}"
            n += 1
        
        # Create flash deal
        FlashDeal.objects.create(
            name=accessory.name,
            description=accessory.description,
            product_type='accessory',
            original_price=accessory.price,
            discount_percentage=discount_percentage,
            sale_price=accessory.sale_price,
            image=accessory.image,
            start_date=timezone.now() - timezone.timedelta(days=1),  # Started yesterday
            end_date=accessory.flash_deal_end or (timezone.now() + timezone.timedelta(days=7)),  # Default 7 days
            is_active=True,
            stock=accessory.stock,
            slug=slug,
            reference_accessory=accessory
        )

class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(transfer_flash_deals),
    ]
