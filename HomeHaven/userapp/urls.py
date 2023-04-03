from django.urls import path
from .views import  *


urlpatterns = [
    path('', index, name='home'),
    path('signin/', signin, name='signin'),
    path('register/', register, name='register'),
    path('verifyotp/<int:user_id>/',verify_otp, name='verifyotp'),
    path('resend-otp/<int:user_id>/', resend_otp, name='resend_otp'),
    path('forgotpass/', forgot_password, name='forgotpass'),
    path('resetpass/<int:user_id>/', reset_password, name='resetpass'),


    path('userproduct/<int:id>/', userproduct, name='userproduct'),
    path('singleproduct/<int:id>/', singleproduct, name='singleproduct'),
    path('search/',search,name="search"),

    path('login/',user_login,name="login"),
    path('logout/',logout, name='logout'),
    path('subscriptionemail/', subscriptionemail , name='subscriptionemail'),


    path('user/', user, name='user'),

    path('orderbook/', orderbook, name='orderbook'),
    path('vieworder/<int:id>/',viewOrder, name='vieworder'),
    path('returnorder/<int:id>/',return_order, name='returnorder'),

    path('useraddress/',address_book, name='useraddress'),
    path('addaddress/<int:id>',add_address, name='addaddress'),
    path('updateprofile',updateprofile,name="updateuserprofile"),
    path('changepass/',changepassword,name="changepassword"),
    path('edit-address/<int:address_id>/',edit_address, name='edit_address'),

    # path('review/<int:product_id>/', review, name='review'),



]
