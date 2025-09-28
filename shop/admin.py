from django.contrib import admin
from django.db.models import F
from .models import Category, Product


@admin.action(description="Set 10%% discount on selected products")
def make_discount_10_percent(modeladmin, request, queryset):
    for product in queryset:
        if not product.original_price:
            product.original_price = product.price
            product.save()

    queryset.update(price=F('price') * 0.9, on_sale=True)


@admin.action(description="Remove discount from selected products")
def remove_discount(modeladmin, request, queryset):
    products_to_update = queryset.filter(original_price__isnull=False)

    for product in products_to_update:
        product.price = product.original_price
        product.original_price = None
        product.on_sale = False
        product.save()


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'original_price', 'on_sale']
    list_filter = ['category', 'on_sale', 'created_at']
    search_fields = ['name', 'description']
    actions = [make_discount_10_percent, remove_discount]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)