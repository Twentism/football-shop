from django.urls import path
from main.views import show_main, create_product, show_product, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_product, delete_product, add_product_entry_ajax, update_product_ajax, delete_product_ajax, ajax_login_user, ajax_register_user, proxy_image, create_product_flutter

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('product/<uuid:id>/', show_product, name='show_product'),
    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path('xml/<uuid:pk>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:pk>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete/', delete_product, name='delete_product'),
    path('create-product-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('update-product-ajax/<uuid:id>/', update_product_ajax, name='update_product_ajax'),
    path('delete-product-ajax/<uuid:id>/', delete_product_ajax, name='delete_product_ajax'),
    path('ajax-login/', ajax_login_user, name='ajax_login_user'),
    path('ajax-register/', ajax_register_user, name='ajax_register_user'),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),
]