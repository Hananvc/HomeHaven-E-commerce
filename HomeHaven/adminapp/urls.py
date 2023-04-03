from django.urls import path
from .import views


urlpatterns = [
    path('',views.adminlogin,name="adminlogin"),
    path('admindash/',views.admindash, name="admindash"),


    path('viewcategory/',views.viewcategory, name="viewcategory"),
    path('addcategory/',views.addcategory, name="addcategory"),
    path('editcategory/<int:pid>/',views.editcategory, name="editcategory"),
    path('deletecategory/<int:pid>/',views.delete_category,name="deletecategory"),


    path('addproduct/',views.addproduct,name="addproduct"),
    path('viewproduct/',views.viewproduct,name="viewproduct"),
    path('editproduct/<int:pid>/',views.editproduct,name="editproduct"),
    path('delete-image/<int:iid>/', views.delete_image, name='deleteimage'),
    path('deleteproduct/<int:pid>/',views.deleteproduct,name="deleteproduct"),


    path('manageuser',views.manageuser,name="manageuser"),
    path('blockuser/<int:id>/',views.blockuser,name="blockuser"),

    path('viewcoupon/',views.view_coupons,name="viewcoupon"),
    path('addcoupon/',views.add_coupons,name="addcoupon"),
    path('editcoupon/<int:pid>/',views.edit_coupon,name="editcoupon"),
    path('deletecoupon/<int:pid>/',views.delete_coupon,name="deletecoupon"),

    path('manageorder/',views.manage_order,name="manageorder"),
    path('updateorder/<int:id>/',views.update_order,name='updateorder'),

    path('salesreport',views.sales_report,name="salesreport"),


    path('adminlogout/',views.adminlogout, name="adminlogout"),

]