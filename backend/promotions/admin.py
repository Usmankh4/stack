from django.contrib import admin
from .models import FlashDeal

@admin.register(FlashDeal)
class FlashDealAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'original_price', 'discount_percentage', 
                   'sale_price', 'start_date', 'end_date', 'is_active', 'stock')
    list_filter = ('product_type', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('sale_price',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'product_type', 'image')
        }),
        ('Pricing', {
            'fields': ('original_price', 'discount_percentage', 'sale_price', 'stock')
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
