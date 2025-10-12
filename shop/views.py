from django.db.models import Count, F, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Category, Product
from .forms import ProductForm

class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(num_products=Count('products'))

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = Category.objects.get(id=self.kwargs['category_id'])
        queryset = Product.objects.filter(category=self.category)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if min_price and min_price.isdigit():
            queryset = queryset.filter(price__gte=min_price)

        if max_price and max_price.isdigit():
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

class SaleProductsView(ListView):
    model = Product
    template_name = 'shop/sale_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(on_sale=True)

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/add_product.html'
    success_url = reverse_lazy('category_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/update_product.html'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.object.id})

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/delete_product_confirm.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('category_list')


class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q', '') # ვიღებთ საძიებო სიტყვას URL-დან
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return Product.objects.none() # თუ საძიებო სიტყვა ცარიელია, არაფერს ვაბრუნებთ