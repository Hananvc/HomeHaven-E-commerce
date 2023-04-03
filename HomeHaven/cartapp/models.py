from django.db import models
from django.contrib.auth.models import User
from userapp.models import Product,Address
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
 


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quantity} x {self.product}"
    
    def sub_total(self):
        return self.product.price * self.quantity
    


class wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class Payment(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(null=True,max_length=30,default='COD')
    refund_id = models.CharField(max_length=30,null=True)
    order_id = models.CharField(max_length=100,blank=True,default='empty')
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField(default=0)
    paid = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.payment_id or 'No order number'


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(500)])
    min_value = models.IntegerField(validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField()
    valid_at = models.DateTimeField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code

class Order(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_total = models.FloatField()
    order_discount = models.FloatField(default=0)
    paid_amount = models.FloatField()
    # tax = models.FloatField()
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.CharField(max_length=50,choices=STATUS,default='Order Confirmed')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    return_reason = models.CharField(max_length=50, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    refund_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.order_number 




class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='user_order_page')
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.name
    def sub_total(self):
        return self.product.price * self.quantity
    

class UserCoupon(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE, null= True)
    coupon = models.ForeignKey(Coupon,on_delete = models.CASCADE, null = True)
    order  = models.ForeignKey(Order,on_delete=models.SET_NULL,null = True,related_name='order_coupon')
    used = models.BooleanField(default = False)
    def __str__(self):
        return str(self.id)