from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from reviews.forms import ProductForm, ReviewForm, UserForm
from reviews.models import Product, Brand, Category, Review, CustomUser


def homepage_view(request):
    all_products = Product.objects.order_by('-id')
    latest_products = all_products[:min(6, all_products.count())]

    products = Product.objects.all()
    products = list(filter(lambda product: product.average_rating() is not None, products))
    products.sort(key=lambda product: product.average_rating(), reverse=True)
    popular_products = products

    products = Product.objects.all()
    products = list(filter(lambda product: product.average_rating() is not None, products))
    products.sort(key=lambda product: product.average_rating())
    least_popular_products = products

    return render(request, 'home.html', {'latest_products': latest_products, 'popular_products': popular_products,
                                         'least_popular_products': least_popular_products})


class IsSuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProductListView(ListView):
    model = Product
    template_name = 'productlist.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        context[self.context_object_name] = Product.objects.filter(Q(name__icontains=q) | Q(brand__name__icontains=q))
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'productdetails.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['review_form'] = ReviewForm(initial={'product': self.object})
        return context


class UserCreateView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('login')
    model = CustomUser
    template_name = 'user_create.html'


class ProductCreateView(LoginRequiredMixin, IsSuperUserMixin, CreateView):
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    model = Product
    template_name = 'productcreate.html'


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brand_details.html'
    context_object_name = 'brand'


class BrandListView(ListView):
    model = Brand
    template_name = 'brandlist.html'
    context_object_name = 'brands'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['genres'] = Genre.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_details.html'
    context_object_name = 'category'


class CategoryListView(ListView):
    model = Category
    template_name = 'categorylist.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['genres'] = Genre.objects.all()
        return context


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_create_view.html'
    success_url = reverse_lazy('home')

    def get_initial(self):
        return {'product': self.request.GET.get('product', 1)}

    def form_valid(self, form):
        if form.is_valid():
            review = form.save(commit=False)
            review.user = self.request.user
            review.save()
            return redirect(reverse_lazy('home'))
        return super().form_valid(form)