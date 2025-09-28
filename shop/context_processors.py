from .models import Product

def latest_products(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    return {'latest_products': latest_products}