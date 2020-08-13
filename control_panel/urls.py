from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    # Auth
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),


    # Customers
    path('customers/', views.customers, name="customers"),
    path('customer/<str:customer_id>', views.customer, name='customer'),


    # Orders
    path('orders/', views.orders, name="orders"),
    path('orders/add/', views.add_order, name='add_order'),
    path('order/<str:order_id>', views.order, name='order'),


    # GiftCards
    path('giftcards/', views.gift_cards, name="giftcards"),
    path('giftcards/add/', views.add_gift_cards, name='add_giftcard'),
    path('giftcard/<str:giftCard_id>', views.gift_card, name='giftcard'),


    # Products
    path('products/', views.products, name="products"),
    path('product/<str:product_id>', views.product, name='product'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/edit/<str:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<str:product_id>/', views.delete_product, name='delete_product'),


    # Transactions
    path('transactions/', views.transactions, name="transactions"),
]
