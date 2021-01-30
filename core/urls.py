from django.urls import path
from .views import (HomeView, ItemDetailView, OrderSummeryView, ItemCategory,
                    CheckoutView, add_to_cart, remove_from_cart, remove_single_item_from_cart, ItemSearch)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<str:category>/', ItemCategory.as_view(), name='item_category'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item/<slug>/',
         remove_single_item_from_cart, name='remove-single-item'),
    path('order-summery/', OrderSummeryView.as_view(), name='order-summery'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('search/', ItemSearch.as_view(), name='item_search'),
]
