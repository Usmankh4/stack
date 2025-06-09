"""
Management command to calculate discounts for products.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import datetime
from store.models import PhoneVariant, Accessory
from promotions.utils import calculate_sale_price, calculate_discount_percentage, apply_discount
from promotions.services.flash_deal_service import FlashDealService


class Command(BaseCommand):
    help = 'Calculate discounts for products and optionally create flash deals'

    def add_arguments(self, parser):
        parser.add_argument('--product-type', type=str, choices=['phone', 'accessory'], required=True,
                            help='Type of product to calculate discounts for')
        parser.add_argument('--product-id', type=int, required=True,
                            help='ID of the product to calculate discounts for')
        
        # Create a mutually exclusive group for discount calculation method
        discount_group = parser.add_mutually_exclusive_group(required=True)
        discount_group.add_argument('--discount', type=float,
                            help='Discount percentage to apply')
        discount_group.add_argument('--sale-price', type=float,
                            help='Custom sale price (discount will be calculated automatically)')
        
        parser.add_argument('--create-deal', action='store_true',
                            help='Create a flash deal with the calculated discount')
        parser.add_argument('--days-active', type=int, default=7,
                            help='Number of days the flash deal should be active (default: 7)')

    def handle(self, *args, **options):
        product_type = options['product_type']
        product_id = options['product_id']
        create_deal = options['create_deal']
        days_active = options['days_active']

        # Get the product
        if product_type == 'phone':
            try:
                product = PhoneVariant.objects.get(id=product_id)
                product_name = f"{product.phone.brand} {product.phone.name} {product.color} {product.storage}"
            except PhoneVariant.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Phone variant with ID {product_id} not found'))
                return
        else:  # accessory
            try:
                product = Accessory.objects.get(id=product_id)
                product_name = product.name
            except Accessory.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Accessory with ID {product_id} not found'))
                return

        # Get original price
        original_price = product.price
        
        # Determine calculation method based on provided arguments
        if options['discount'] is not None:
            # Calculate sale price from discount percentage
            discount_percentage = Decimal(str(options['discount']))
            sale_price = calculate_sale_price(original_price, discount_percentage)
            savings = original_price - sale_price
            calculation_method = "discount_to_price"
        else:
            # Calculate discount percentage from sale price
            sale_price = Decimal(str(options['sale_price']))
            discount_percentage = calculate_discount_percentage(original_price, sale_price)
            savings = original_price - sale_price
            calculation_method = "price_to_discount"

        # Display results
        self.stdout.write(self.style.SUCCESS(f'Product: {product_name}'))
        self.stdout.write(self.style.SUCCESS(f'Original price: ${original_price}'))
        self.stdout.write(self.style.SUCCESS(f'Discount: {discount_percentage}%'))
        self.stdout.write(self.style.SUCCESS(f'Sale price: ${sale_price}'))
        self.stdout.write(self.style.SUCCESS(f'Customer saves: ${savings}'))

        # Create flash deal if requested
        if create_deal:
            now = timezone.now()
            start_date = now
            end_date = now + datetime.timedelta(days=days_active)

            if calculation_method == "discount_to_price":
                flash_deal = FlashDealService.create_flash_deal_from_product(
                    product=product,
                    discount_percentage=discount_percentage,
                    start_date=start_date,
                    end_date=end_date,
                    name=f"{product_name} {discount_percentage}% Off Deal"
                )
            else:  # price_to_discount
                flash_deal = FlashDealService.create_flash_deal_with_custom_price(
                    product=product,
                    sale_price=sale_price,
                    start_date=start_date,
                    end_date=end_date,
                    name=f"{product_name} Special Deal - Now ${sale_price}"
                )

            self.stdout.write(self.style.SUCCESS(f'Created flash deal: {flash_deal.name}'))
            self.stdout.write(self.style.SUCCESS(f'Active from: {flash_deal.start_date.strftime("%Y-%m-%d %H:%M")}'))
            self.stdout.write(self.style.SUCCESS(f'Active until: {flash_deal.end_date.strftime("%Y-%m-%d %H:%M")}'))
            self.stdout.write(self.style.SUCCESS(f'Deal slug: {flash_deal.slug}'))
