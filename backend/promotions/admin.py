from django.contrib import admin
from django.utils.html import format_html
from .models import FlashDeal

@admin.register(FlashDeal)
class FlashDealAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'original_price', 'discount_percentage', 
                   'sale_price', 'start_date', 'end_date', 'is_active', 'stock')
    list_filter = ('product_type', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('price_calculator',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'product_type', 'image')
        }),
        ('Pricing', {
            'fields': ('original_price', 'discount_percentage', 'sale_price', 'price_calculator', 'stock'),
            'description': 'You can either set the discount percentage or the sale price. The other value will be calculated automatically.'
        }),
        ('Availability', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('References', {
            'fields': ('reference_phone', 'reference_accessory'),
            'classes': ('collapse',)
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.product_type == 'phone':
            form.base_fields['reference_accessory'].disabled = True
        elif obj and obj.product_type == 'accessory':
            form.base_fields['reference_phone'].disabled = True
        return form
        
    def price_calculator(self, obj=None):
        """
        Add JavaScript to automatically calculate sale price or discount percentage
        when the other value changes.
        """
        if obj is None:
            return ""
            
        script = """
        <script type="text/javascript">
            (function($) {
                $(document).ready(function() {
                    // Get the form fields
                    var originalPriceField = $('#id_original_price');
                    var discountField = $('#id_discount_percentage');
                    var salePriceField = $('#id_sale_price');
                    
                    // Function to calculate sale price from discount
                    function calculateSalePrice() {
                        var originalPrice = parseFloat(originalPriceField.val());
                        var discount = parseFloat(discountField.val());
                        
                        if (!isNaN(originalPrice) && !isNaN(discount)) {
                            var salePrice = originalPrice - (originalPrice * discount / 100);
                            salePriceField.val(salePrice.toFixed(2));
                        }
                    }
                    
                    // Function to calculate discount from sale price
                    function calculateDiscount() {
                        var originalPrice = parseFloat(originalPriceField.val());
                        var salePrice = parseFloat(salePriceField.val());
                        
                        if (!isNaN(originalPrice) && !isNaN(salePrice) && originalPrice > 0) {
                            var discount = ((originalPrice - salePrice) / originalPrice) * 100;
                            discountField.val(discount.toFixed(2));
                        }
                    }
                    
                    // Add event listeners
                    discountField.on('input', calculateSalePrice);
                    salePriceField.on('input', calculateDiscount);
                    originalPriceField.on('input', function() {
                        // When original price changes, recalculate based on discount
                        calculateSalePrice();
                    });
                });
            })(django.jQuery);
        </script>
        """
        return format_html(script)
