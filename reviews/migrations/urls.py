from django.urls import path

from reviews import views

urlpatterns = [
    path('', views.homepage_view, name='home'),

    path('product/add/', views.ProductCreateView.as_view(), name='product-add'),
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('brand/', views.BrandListView.as_view(), name='brand_list'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('brand/<int:pk>/', views.BrandDetailView.as_view(), name='brand_details'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_details'),
    path('review/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('create-user/', views.UserCreateView.as_view(), name='create-user'),
]