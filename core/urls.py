from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<str:category>/',
         views.ItemCategory.as_view(), name='item_category'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/',
         views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item/<slug>/',
         views.remove_single_item_from_cart, name='remove-single-item'),
    path('order-summery/', views.OrderSummeryView.as_view(), name='order-summery'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('search/', views.ItemSearch.as_view(), name='item_search'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
]
