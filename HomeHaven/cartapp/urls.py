from . import views
from django.urls import path

urlpatterns = [
    path('',views.viewcart,name="viewcart"),
    path('add-to-cart/<int:product_id>/',views.addtocart,name="add_to_cart"),
    path('removecartitem/<int:product_id>/',views.removecartitem,name='removecartitem'),
    path('addcartitem/<int:product_id>/',views.addcartitem,name='addcartitem'),
    
    path('removecartproduct/<int:product_id>/',views.removecartproduct,name='removecartproduct'),

    path('wishlist/',views.userwishlist,name='userwishlist'),
    path('addwishlist/<int:product_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('removewishlist/<int:product_id>/',views.remove_from_wishlist,name='remove_from_wishlist'),

    path('checkout/',views.checkout, name='checkout'),
    path('confirmation/',views.confirmation, name='confirmation'),

    
    path('order-complete/<str:ordernumber>/',views.orderComplete, name='order_complete'),
    path('place_order/', views.placeOrder, name='place_order'),

    
    path('proceed_to_pay/',views.razorPayCheck,name="razorpaycheck"),
    path('cancel-order/<int:id>/',views.cancelOrder, name='cancel_order'),



]
