from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='logout'),

    path('product_list', views.product_list, name='product_list'),  
    path('product_create', views.product_create, name='product_create'),  
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),  
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),  

    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('place_order/', views.place_order, name='place_order'),
    path('order_list/', views.user_orders, name='order_list'),
    path('my_orders/', views.user_orders, name='user_orders'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)