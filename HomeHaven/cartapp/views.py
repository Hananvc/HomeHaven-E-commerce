from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from userapp.models import Product,Address
from django.contrib import messages
from userapp.views import user_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime,random
from django.http import JsonResponse
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache
import HomeHaven.settings




# Create your views here.

@never_cache
@login_required(login_url='login')
def viewcart(request):
    if request.user.is_authenticated:
        current_user = request.user

        items = CartItem.objects.filter(user_id=current_user.id).order_by('id')
        cart_items = []
        total = 0
        for cart_item in items:
            product = get_object_or_404(Product, id=cart_item.product_id)
            quantity = cart_item.quantity
            price = product.price*quantity
            cart_items.append({'product':product,'quantity':quantity,'price':price}) 
            if product.stock == 0:
                pass
            else:
                total += price   
        context = { 'cart_items': cart_items, 'total': total }

    else:
        messages.warning(request, "Please log in to add items to cart.")
        return redirect(user_login)
    return render(request, 'cart/viewcart.html',context)

@never_cache
@login_required(login_url='login')
def addtocart(request, product_id):
    if request.user.is_authenticated :
        current_user=request.user
        quantity = request.POST.get('quantity')
        if quantity is None:
            product_quantity = 1
        else:
            product_quantity= int(quantity)

        product = get_object_or_404(Product, id=product_id)

        item_exists = CartItem.objects.filter(user_id=current_user.id,product_id=product.id).exists()
        if (item_exists):
            item=CartItem.objects.get(product_id=product.id,user_id=current_user.id)
            quantity_expected=item.quantity + product_quantity
            if product.stock>quantity_expected:

                item.quantity = item.quantity + product_quantity
                item.save()
                messages.success(request,  f"{product_quantity} pieces of {product.name} are added to Cart.")
            else:

                item.quantity = product.stock
                item.save()
                messages.info(request,  f"{product.stock} items left. All of them are added to Cart.")
        else:
            if(product.stock>=product_quantity):
                item = CartItem.objects.create(user_id=current_user.id, product_id=product.id,quantity=product_quantity)
                messages.success(request, f"{product_quantity} pieces of {product.name} are added to Cart.")
            else:
                product_quantity = product.stock
                item = CartItem.objects.create(user_id=current_user.id, product_id=product.id,quantity=product_quantity)
                messages.info(request,  f"{product.stock} items left. All of them are added to Cart.")

        return redirect(viewcart)
    else:
        messages.warning(request, "Please log in to add items to cart.")
        return redirect(user_login)



def addcartitem(request,product_id):
    if request.user.is_authenticated :
        current_user=request.user
        product = get_object_or_404(Product, id=product_id)
        item=CartItem.objects.get(user_id=current_user.id, product=product)
        item.quantity = item.quantity + 1
        if (product.stock>item.quantity):
            item.save()
            return redirect(viewcart)
        else:
            messages.warning(request,"Product Out Of Stock...! Can't be added to cart")
            return redirect(viewcart)

    else:
        messages.warning(request, "Please log in to add items to cart.")
        return redirect(user_login)



def removecartitem(request,product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)

    cart_items = CartItem.objects.filter(user_id=current_user.id, product=product)
    for cart_item in cart_items:
        if cart_item.quantity == 1:
            cart_item.delete()  # remove the item from the cart if the quantity is 1
        else:
            cart_item.quantity -= 1
            cart_item.save()  # decrement the quantity by 1
    return redirect(viewcart)


def removecartproduct(request,product_id):
    current_user = request.user
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(user_id=current_user.id,product_id=product.id)
    cart_item.delete()
    return redirect(viewcart)




@never_cache
@login_required(login_url='login')
def userwishlist(request):
    user = request.user
    witems=wishlist.objects.filter(user_id=user.id)
    witem_count = witems.count()
    context={
        'witems':witems,
        'witem_count':witem_count,
    }
    return render(request,'cart/wishlist.html',context)


def add_to_wishlist(request,product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        user = request.user
        if wishlist.objects.filter(product=product,user_id=user.id).exists():
            messages.info(request, "Product already exist in wishlist")
            return redirect(userwishlist)
            
        else:
            wishlist.objects.create(product=product,user_id=user.id)
            return redirect(userwishlist)
    else:
        return redirect(user_login)


def remove_from_wishlist(request,product_id):
    user = request.user
    wishItem=wishlist.objects.get(product_id=product_id,user_id=user.id)
    wishItem.delete()
    return redirect(userwishlist)

@never_cache
@login_required(login_url='login')
def checkout(request, address_id=None):
    allcoupon=Coupon.objects.all()
    subtotal=0
    quantity=0
    amountToBePaid =0
    msg=''
    cart_items=None
    coupon_discount = 0
    coupon_code = ''
    discount = False
    coupon = ''
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
    if address_id:
        addresses = Address.objects.filter(id=address_id, user_id=request.user)
    else:
        addresses = Address.objects.filter(user_id=request.user)
    
    user=User.objects.get(id=request.user.id)
    cart_items=CartItem.objects.filter(user=user, product__stock__gt=0)
    
    for cart_item in cart_items:
        subtotal+=(cart_item.product.price*cart_item.quantity)
        quantity+=cart_item.quantity
    grand_total = subtotal+70
    amountToBePaid = grand_total
    if ('couponCode' in request.POST):
            coupon_code = request.POST.get('couponCode')
            try:
                coupon = Coupon.objects.get(code = coupon_code)
                grand_total = request.POST['grand_total']
                coupon_discount = 0
                if (coupon.active):
                    try:
                        instance = UserCoupon.objects.get(user=request.user, coupon=coupon)
                    except ObjectDoesNotExist:
                        instance = None
                    
                    if(instance):
                        pass
                    else:
                        instance = UserCoupon.objects.create(user = request.user ,coupon = coupon)
                    if(not instance.used):
                        if float(grand_total) >= float(instance.coupon.min_value):
                            coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
                            amountToBePaid = float(grand_total) - coupon_discount
                            amountToBePaid = format(amountToBePaid, '.2f')
                            coupon_discount = format(coupon_discount, '.2f')
                            msg = 'Coupon Applied successfully'
                            discount=True
                        else:
                            msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
                    else:
                        msg = 'Coupon is already used'
                else:
                    msg="Coupon is not Active!"
            except:
                msg="Invalid Coupon Code!"
    else:
            try:
                instance = UserCoupon.objects.get(user=request.user, used= False)
                instance.delete()
            except ObjectDoesNotExist:
                instance = None
    
    context={
        'subtotal':subtotal,
        'quantity':quantity,
        'cart_items':cart_items,
        'grand_total':grand_total,
        'user':user,
        'amountToBePaid':amountToBePaid,
        'msg':msg,
        'coupon':coupon,
        'coupon_discount':coupon_discount,
        'discount':discount,
        'AllAddress':addresses,
        'city' :city,
        'state':state,
        'allcoupon':allcoupon,
    }


    return render(request,'cart/checkout.html',context)

@never_cache
@login_required(login_url='login')
def confirmation(request):
    try:
        cart_items=CartItem.objects.filter(user=request.user)
        newAddress_id = request.POST.get('selected_addresses')
        total=request.POST.get('total')
        grand_total=request.POST.get('grand_total')
        amountToBePaid=request.POST.get('amountToBePaid')
        couponCode=request.POST.get('couponCode')
        couponDiscount=request.POST.get('couponDiscount')
        
       
        
        
        if not newAddress_id:
            messages.error(request,'Select An Address to Proceed to Checkout.')
            return redirect(checkout)
        else:
            address  = Address.objects.get(id = newAddress_id)

    except ObjectDoesNotExist:
        pass
    context={
        'cart_items':cart_items,
        'addressSelected':address,
        'couponDiscount':couponDiscount,
        'couponCode':couponCode,
        'grand_total':grand_total,
        'amountToBePaid':amountToBePaid,
        'total':total

        
    }
    return render (request,'cart/confirmation.html',context)

def calculateCartTotal(request):
   cart_items   = CartItem.objects.filter(user=request.user)
   if not cart_items:

       pass
   else:
      total = 0
      tax=0
      grand_total=0

      for cart_item in cart_items:
         total    += (cart_item.product.price * cart_item.quantity)
         tax = 70
         grand_total = tax + total
   return total, tax, grand_total



@never_cache
@login_required(login_url='login')
def placeOrder(request):
   if request.method =='POST':
         if ('couponCode' in request.POST):
            instance = checkCoupon(request)

         cart_items   = CartItem.objects.filter(user=request.user)
         if not cart_items:
            return redirect('userproduct',0)
         
         newAddress_id = request.POST.get('addressSelected')
         address  = Address.objects.get(id = newAddress_id)
         newOrder =Order()
         newOrder.user=request.user
         newOrder.address = address
         yr = int(datetime.date.today().strftime('%Y'))
         dt = int(datetime.date.today().strftime('%d'))
         mt = int(datetime.date.today().strftime('%m'))
         d = datetime.date(yr,mt,dt)
         current_date = d.strftime("%Y%m%d")
         rand = str(random.randint(1111111,9999999))
         order_number = current_date + rand
         newPayment = Payment()
       
         newPayment.payment_id = request.POST.get('payment_id')

         payment_id  =order_number
         newPayment.payment_method = request.POST.get('payment_method')
         newPayment.customer = request.user
         newPayment.save()
         newOrder.payment = newPayment
         total, tax, grand_total = calculateCartTotal(request)
         newOrder.order_total = grand_total
         if(instance):
            if(instance.used == False):
                if float(grand_total) >= float(instance.coupon.min_value):
                    coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
                    amountToBePaid = float(grand_total) - coupon_discount
                    amountToBePaid = format(amountToBePaid, '.2f')
                    coupon_discount = format(coupon_discount, '.2f')
                    newOrder.order_discount = coupon_discount
                    newOrder.paid_amount = amountToBePaid
                    instance.used = True
                    newOrder.paid_amount = amountToBePaid
                    newPayment.amount_paid = amountToBePaid
                    instance.save()
                else:
                    msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
            else:
                newOrder.paid_amount = grand_total
                newPayment.amount_paid = grand_total
                newOrder.discount=0
                msg = 'Coupon is not valid'
         else:
            newOrder.paid_amount = grand_total
            newPayment.amount_paid = grand_total
            msg = 'Coupon not Added'
         newPayment.save()
         newOrder.payment = newPayment
         order_number = 'HH'+ order_number
         newOrder.order_number =order_number
         #to making order number unique
         while Order.objects.filter(order_number=order_number) is None:
            order_number = 'HH'+order_number
         newOrder.tax=tax
         newOrder.save()
         newPayment.order_id = newOrder.id
         newPayment.save()
         newOrderItems = CartItem.objects.filter(user=request.user)
         for item in newOrderItems:
            OrderProduct.objects.create(
                order = newOrder,
                customer=request.user,
                product=item.product,
                product_price=item.product.price,
                quantity=item.quantity
            )
            #TO DECRESE THE QUANTITY OF PRODUCT FROM CART
            orderproduct = Product.objects.filter(id=item.product_id).first()
            if(orderproduct.stock<=0):
               messages.warning(request,'Sorry, Product out of stock!')
               orderproduct.is_available = False
               orderproduct.save()
               item.delete()
               return redirect('viewcart')
            elif(orderproduct.stock < item.quantity):
               messages.success(request,  f"{orderproduct.stock} only left in cart.")
               return redirect('viewcart')
            else:
               orderproduct.stock -=  item.quantity
            orderproduct.save()
         if(instance):
            instance.order = newOrder
            instance.save()
        # TO CLEAR THE USER'S CART
         cart_item=CartItem.objects.filter(user=request.user)
         cart_item.delete()
         messages.success(request,'Order Placed Successfully')
         payMode =  request.POST.get('payment_method')
         if (payMode == "Paid by Razorpay" ):
            return JsonResponse ({'ordernumber':order_number,'status':"Your order has been placed successfully"})
         elif (payMode == "COD" ):
            request.session['my_context'] = {'payment_id':payment_id}
            return redirect('order_complete', order_number )
   return redirect('checkout')


def checkCoupon(request):
   try:
      coupon_code = request.POST.get('couponCode')
      coupon = Coupon.objects.get(code = coupon_code)
      try:
         instance = UserCoupon.objects.get(user=request.user, coupon=coupon)
      except ObjectDoesNotExist:
         instance = None
         if(instance):
            pass
         else:
            instance = UserCoupon.objects.create(user = request.user ,coupon = coupon)
   except:
      instance = None
   return instance




@never_cache
@login_required(login_url='login')
def razorPayCheck(request):
   total=0
   coupon_discount =0
   amountToBePaid = 0
   current_user=request.user
   cart_items=CartItem.objects.filter(user_id=current_user.id)
   if cart_items:
      for cart_item in cart_items:
         total+=(cart_item.product.price*cart_item.quantity)
      grand_total=total+70
      grand_total = round(grand_total,2)
      try:
         instance = UserCoupon.objects.get(user=request.user, used=False)
         coupon = instance.coupon.code
         if float(grand_total) >= float(instance.coupon.min_value):
            coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
            amountToBePaid = float(grand_total) - coupon_discount
            amountToBePaid = format(amountToBePaid, '.2f')
            coupon_discount = format(coupon_discount, '.2f')
      except ObjectDoesNotExist:
         instance = None
         amountToBePaid = grand_total
         coupon_discount = 0
         coupon =None
      return JsonResponse({
         'grand_total' : grand_total,
         'coupon': coupon,
         'coupon_discount':coupon_discount,
         'amountToBePaid':amountToBePaid
      })
   else:
      return redirect('userproduct',0)
   
def orderComplete(request,ordernumber) :

    order = Order.objects.get(user=request.user,order_number=ordernumber)
    orderitem = OrderProduct.objects.filter(customer=request.user,order=order)

    return render(request,'cart/order_completed.html',locals())

@never_cache
@login_required(login_url='login')
def cancelOrder(request, id):
    client = razorpay.Client(auth=(HomeHaven.settings.API_KEY, HomeHaven.settings.RAZORPAY_SECRET_KEY))
    order = Order.objects.get(id=id, user=request.user)
    payment = order.payment
    msg = ''

    if payment.payment_method == 'Paid by Razorpay':
        payment_id = payment.payment_id
        amount = payment.amount_paid
        amount = amount * 100
        captured_amount = client.payment.capture(payment_id,amount)

        if captured_amount['status'] == 'captured':
            refund_data = {
                "payment_id": payment_id,
                "amount": amount,  # amount to be refunded in paise
                "currency": "INR",
            }
        else:
            msg = "Your bank has not completed the payment yet."
            messages.error(request, msg)
            orderitems = OrderProduct.objects.filter(order=order)
            context = {
                'order': order,
                'orderitems': orderitems,
                'msg': msg
            }
            return render(request, 'user/orderview.html', context)

        refund = client.payment.refund(payment_id, refund_data)

        if refund is not None:
            current_user = request.user
            order.refund_completed = True
            order.status = 'Cancelled'
            payment = order.payment
            payment.refund_id = refund['id']
            payment.save()
            order.save()
            msg = "Your order has been successfully cancelled and amount has been refunded!"
            mess = f'Hello\t{current_user.first_name},\nYour order has been canceled,Money will be refunded with in 1 hour\nThanks!'
            send_mail(
                "The Homehaven  - Order Cancelled",
                mess,
                settings.EMAIL_HOST_USER,
                [current_user.username],
                fail_silently=False
            )
            messages.success(request, msg)
        else:
            msg = "Your order is not cancelled because the refund could not be completed now. Please try again later. If the issue continues, CONTACT THE SUPPORT TEAM!"
            messages.error(request, msg)
            pass
    else:
        if payment.paid:
            order.refund_completed = True
            order.status = 'Cancelled'
            msg = "YOUR ORDER HAS BEEN SUCCESSFULLY CANCELLED!"
            order.save()
            messages.success(request, msg)
        else:
            order.status = 'Cancelled'
            order.save()
            msg = "Your payment has not been received yet. But the order has been cancelled."
            messages.warning(request, msg)

    orderitems = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'orderitems': orderitems,
        'msg': msg
    }
    return render(request, 'user/orderview.html',context)
