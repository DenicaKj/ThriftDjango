"""
URL configuration for finalenThrift project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path

import Thrift.views
from Thrift.views import index, register_request,delete_product,delivery_info, arrived_product, for_sending, product_details, profile, \
    remove_from_cart, add_to_cart, \
    cart, favorites, login_request, logout_request, add_product, remove_from_favorites, female, male, add_to_favorites, \
    sent, arrived, sold,buy_products,sent_product,sent_2,accepted,all_bought,all_sold,add_comment,delete_comment,edit_product,payment
from django.conf.urls.static import static

handler404 = 'Thrift.views.error_404'
handler500 = 'Thrift.views.error_500'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('index/', index, name='index'),
    path('cart/', cart, name='cart'),
    path("register", register_request, name="register"),
    path("add_product", add_product, name="add_product"),
    path("add_to_favorites", add_to_favorites, name="add_to_favorites"),
    path("remove_from_favorites", remove_from_favorites, name="remove_from_favorites"),
    path("add_to_cart", add_to_cart, name="add_to_cart"),
    path('product/<int:pk>/', product_details, name='product-details'),
    path('delete_product/<int:pk>/', delete_product, name='delete_product'),
    path('add_comment/', add_comment, name='add_comment'),
    path('delete_comment/', delete_comment, name='delete_comment'),
    path('profile/<int:pk>/', profile, name='profile'),
    path('edit_product/<int:pk>/', edit_product, name='edit_product'),
    path("remove_from_cart", remove_from_cart, name="remove_from_cart"),
    path("favorites", favorites, name="favorites"),
    path("for_sending", for_sending, name="for_sending"),
    path("sent", sent, name="sent"),
    path("sent_2", sent_2, name="sent_2"),
    path("sold", sold, name="sold"),
    path("all_bought", all_bought, name="all_bought"),
    path("all_sold", all_sold, name="all_sold"),
    path("accepted", accepted, name="accepted"),
    path("buy_products", buy_products, name="buy_products"),
    path("arrived", arrived, name="arrived"),
    path("arrived_product/<int:pk>/", arrived_product, name="arrived_product"),
    path("delivery_info/<int:pk>/", delivery_info, name="delivery_info"),
    path("sent_product/<int:pk>/", sent_product, name="sent_product"),
    path("female", female, name="female"),
    path("male", male, name="male"),
    path("login", login_request, name="login"),
    path("payment", payment, name="payment"),
    path("accounts/login/", login_request, name="accounts/login"),
    path("logout", logout_request, name= "logout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
