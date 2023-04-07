from django.shortcuts import render,HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from userapp.models import *
from django.db.models import Sum
import os
from cartapp.forms import CouponForm
from cartapp.models import *
from datetime import datetime
from django.views.decorators.cache import cache_control
# Create your views here.

def adminlogin(request):
    if request.user.is_superuser:
        return redirect('admindash')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.info(request,"User login succesfull")
            return redirect('admindash')
        else:
            messages.error(request, "Username or password mismatch")
    return render(request, 'admin/admin_login.html')

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admindash(request):
    user=User.objects.all().count()
    product=Product.objects.all().count()
    allcategory = Category.objects.all()
    category=allcategory.count()
    order=Order.objects.all().count()
    coupons=Coupon.objects.all().count()
    total_income = Payment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum']
    refunded = Payment.objects.filter(refund_id=None)
    refund_income = refunded.aggregate(Sum('amount_paid'))['amount_paid__sum']
    cod_sum = Payment.objects.filter(payment_method='COD' ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    cod_sum = round(cod_sum,2)
    razorpay_sum = Payment.objects.filter(payment_method='Paid by Razorpay').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    

    
            
    context={
        'user':user,
        'product':product,
        'category':category,
        'order':order,
        'coupons':coupons,
        'total_income' :total_income,
        'razorpay_sum':razorpay_sum,
        'cod_sum':cod_sum,
        'allcategory':allcategory,

    }

    return render(request, 'admin/admin_dash.html' , context)



@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewcategory(request):
    category = Category.objects.all().order_by('id')
    dict_user={
        'categories':category
    }
    return render(request, 'admin/viewcategory.html',dict_user)

@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def addcategory(request):
    if request.method == 'POST':
        name = request.POST['name']
        images = request.FILES.get('images')
        if Category.objects.filter(name__iexact=name.lower().replace(' ', '')).exists():
            messages.info(request, "Category already exists")

        else:
            Category.objects.create(name=name,image=images)
            messages.success(request, "Category added successfully")
            return redirect(viewcategory)
    return render(request, 'admin/addcategory.html')

@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def editcategory(request,pid):
    category = Category.objects.get(id=pid)
    if request.method == 'POST':
        name = request.POST['name']
        images = request.FILES.get('images')
        category.name = name
        if images is not None:
            category.image=images
        category.save()
        messages.success(request,'Category edited successfully')
        return redirect(viewcategory)
    return render(request, 'admin/editcategory.html',locals())    

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.info(request,'Category deleted successfully')
    return redirect(viewcategory)


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def addproduct(request):
    category = Category.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        categ = request.POST['categories']
        desc = request.POST['desc']
        images = request.FILES.getlist('image')
        stock = request.POST['stock']
        catobj = Category.objects.get(id=categ)
        product = Product.objects.create(name=name, price=price, category=catobj, description=desc ,stock=stock)
        product.save()
        for image in images:
            ProductImage.objects.create(product=product, images=image)
        messages.success(request, "Product Added")
        return redirect(viewproduct)


    return render(request, 'admin/add_product.html',locals())


@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def viewproduct(request):
    product = Product.objects.all().order_by('id')
    dict_prod = {
        'product' : product,
    }
    return render(request, 'admin/view_product.html',dict_prod)


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def editproduct(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    images = ProductImage.objects.filter(product=product)
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        desc = request.POST['desc']
        stock = request.POST['stock']
        catobj = Category.objects.get(id=cat)
        
        if int(price) < 0:
            messages.warning(request,"Enter a valid quantity")
            return redirect(editproduct,pid)
        else:

        # Update product attributes
            Product.objects.filter(id=pid).update(name=name, price=price, category=catobj, description=desc ,stock=stock)

        # Get the new images uploaded during editing
        new_images = request.FILES.getlist('images')

        # Add the new images to the product
        for image in new_images:
            ProductImage.objects.create(product=product, images=image)
       
        messages.success(request, "Product Updated")
        return redirect(viewproduct)
    return render(request, 'admin/edit_product.html', locals())

@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def delete_image(request, iid):
    image = ProductImage.objects.get(id=iid)
    image_path = os.path.join(settings.MEDIA_ROOT, str(image.images))
    os.remove(image_path)
    product_id = image.product.id if image.product else None
    image.delete()
    if product_id:
        return HttpResponseRedirect(reverse(editproduct, args=[product_id]))
    else:
        return HttpResponseRedirect(reverse(viewproduct))


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteproduct(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect(viewproduct)

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def manageuser(request):
    user = User.objects.all().order_by('id')[1:]

    return render(request, 'admin/manage_user.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def blockuser(request, id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        messages.success(request, "user has been blocked.")
    else:
        user.is_active = True
        messages.success(request, "user has been unblocked.")
    user.save()
    return redirect(manageuser)


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def view_coupons(request):
    coupons = Coupon.objects.all()
    return render(request,'admin/view_coupon.html',{'coupons':coupons})


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(view_coupons)
    else:
        form = CouponForm()
    return render(request, 'admin/add_coupon.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def edit_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)

    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon Updated")
            return redirect(view_coupons)
    else:
        form = CouponForm(instance=coupon)

    return render(request, 'admin/edit_coupon.html', {'form': form, 'coupon': coupon})

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delete_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)
    coupon.delete()
    messages.success(request, "Coupon Deleted")
    return redirect(view_coupons)

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def manage_order(request):
    orders=Order.objects.all().order_by('created_at')
    return render(request, 'admin/manage_order.html', locals())

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def update_order(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        status = request.POST.get('status')
        if(status):
            order.status = status
            order.save()
        if status  == "Delivered":
            try:
                payment = Payment.objects.get(payment_id = order.order_number, status = False)
                if payment.payment_method == 'Cash on Delivery':
                    payment.paid = True
                    payment.save()
            except:
                pass
    return redirect(manage_order)

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def sales_report(request):
    fro=request.GET.get('from_date')
    to=request.GET.get('to_date')
    
    if fro and to :
        orders = Order.objects.all().order_by('-id')
        today_date = datetime.now().strftime('%Y-%m-%d')

        if 'from_date' in request.GET and 'to_date' in request.GET:
            from_date = request.GET['from_date']
            to_date = request.GET['to_date']

            if to_date > today_date:
                messages.warning(request, "Please select a date up to today's date.")
            elif from_date > to_date:
                messages.warning(request, "The from date should be before than the To date")
            else:
                orders = orders.filter(created_at__range=[from_date, to_date])
                total_sales = orders.aggregate(Sum('paid_amount'))['paid_amount__sum']
    else:
        orders = Order.objects.all().order_by('-id')
       
       
    return render(request, 'admin/sales_report.html', locals())


def adminlogout(request):
    auth.logout(request)
    if 'username' in request.session:
            request.session.flush()
    return redirect(adminlogin)
