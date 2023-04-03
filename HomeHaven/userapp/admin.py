from django.contrib import admin
from .models import Product,ProductImage,Category,Address,UserProfile,Review

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(UserProfile)
admin.site.register(Review)