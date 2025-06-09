from django.contrib import admin
from .models import Phones, PhoneVariant, Accessory

@admin.register(Phones)
class PhonesAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'slug')
    list_filter = ('brand',)
    search_fields = ('name', 'brand')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PhoneVariant)
class PhoneVariantAdmin(admin.ModelAdmin):
    list_display = ('sku', 'phone', 'color', 'storage', 'price', 'stock', 'is_active', 'is_new_arrival', 'is_best_seller')
    list_filter = ('is_active', 'is_new_arrival', 'is_best_seller', 'phone__brand')
    search_fields = ('sku', 'phone__name', 'color', 'storage')
    list_editable = ('price', 'stock', 'is_active', 'is_new_arrival', 'is_best_seller')

@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active', 'is_new_arrival', 'is_best_seller')
    list_filter = ('is_active', 'is_new_arrival', 'is_best_seller')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_active', 'is_new_arrival', 'is_best_seller')
