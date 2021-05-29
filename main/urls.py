from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('about', views.about, name='about'),
    path('cart', views.cart, name='cart'),
    path('cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<id>', views.remove_from_cart, name='remove-cart'),
    path('cart/inc/<id>', views.increase, name='increment'),
    path('cart/dec/<id>', views.decrease, name='decrement'),
    path('profile', views.profile, name='profile'),
    path('Babies&Toys', views.toys, name='Babies&Toys'),
    path('Electronic_Accessories', views.accessories, name='Electronic_Accessories'),
    path('Electronic_Gadgets', views.gadgets, name='Electronic_Gadgets'),
    path('Groceries', views.groceries, name='Groceries'),
    path('Health&Beauty', views.health, name='Health&Beauty'),
    path('Home_Appliances', views.home, name='Home_Appliances'),
    path('Liquor', views.liquor, name='liquor'),
    path('MenFashion', views.MenFashion, name='MenFashion'),
    path('Sports&Outdoor', views.sport, name='Sports&Outdoor'),
    path('WomenFashion', views.WomenFashion, name='WomenFashion'),
    path('checkout', views.checkout, name='checkout'),
    path('shipment', views.Shipment, name='shipment'),
    path('search', views.search, name='search'),
    path('khaltiverify', views.khaltiverify, name='khaltiverify'),
    path('orders', views.admin, name='admin')

]
