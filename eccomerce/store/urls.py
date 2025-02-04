from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path('', views.all_products, name='all_products'),
    path('item/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('order-confirmation/',views.order_confirmation,name='order_confirmation'),
    path('add_cart/',views.addcart,name='addcart'),
    path('order/',views.order,name='order'),
    path('orderreceived/',views.rozarpayverify,name="orderreceived"),
   


]