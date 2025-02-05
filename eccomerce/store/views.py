from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout
import razorpay
from django.contrib import messages 
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from razorpay.errors import BadRequestError
razorpay_client = razorpay.Client(
    auth=(settings.ROZARPAY_KEY, settings.RAZOR_KEY_SECRET))

def cart_sessions(request):
    carts=request.session.session_key 
    print('carts===',carts)
    if not carts:
       carts=request.session.create()
       print(carts)
    return carts  

def user_login(request):
     
  
     if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            
            if user is not None  and user.is_active == True:
             
                    try:
                         carts = Cart.objects.all()
                         try:
                                car=CartItem.objects.get(user=user,cart_id__in=[x.id for x in carts])
                                # c1=Cart.objects.all()
                                # c2=CartItem.objects.filter(cart)
                                print('car',car)
                         except CartItem.DoesNotExist:
                                carts = Cart.objects.get(cart_id=cart_sessions(request))
                                cart_exists = CartItem.objects.filter(cart=carts).exists()
                                if cart_exists:
                                    cart_items = CartItem.objects.filter(cart=carts)
                                    for item in cart_items:
                                        item.user = user
                                        item.save()
                    except CartItem.DoesNotExist:
                            carts = Cart.objects.get(cart_id=cart_sessions(request))
                            cart_exists = CartItem.objects.filter(cart=carts).exists()
                            if cart_exists:
                                cart_items = CartItem.objects.filter(cart=carts)
                                for item in cart_items:
                                    item.user = user
                                    item.save()
                
                    login(request, user)
                    return redirect('store:all_products')
            else:
                form = LoginForm()
                return render(request,'store/login.html',{'form':form})

     else:
            form = LoginForm()
            return render(request,'store/login.html',{'form':form})

     return render(request,'store/login.html')


def signup(request):
    if request.method == "POST":
       form = SignupForm(request.POST)
       if form.is_valid():
            User.objects.create(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                mobile=form.cleaned_data['mobile'],
                password=make_password(form.cleaned_data['password']),
            )
            return redirect('store:login')  # Replace with your desired redirect
    else:
         form = SignupForm()
         return render(request,'store/signup.html',{'form':form})

      

    return render(request,'store/signup.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('store:login')




def all_products(request):
    products = Product.products.all()
    return render(request, 'store/home.html', {'products': products})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    if request.user.is_authenticated:
        try:
            cartitem=CartItem.objects.get(product_id=product.id,user=request.user)
        except CartItem.DoesNotExist:
            cartitem=None

    else:
         try:
                cart=Cart.objects.get(cart_id=cart_sessions(request))
                cartitem=CartItem.objects.filter(product_id=product.id,cart_id=cart).exists()
         except Cart.DoesNotExist:
                cart=None
                cartitem=None

    return render(request, 'store/products/detail.html', {'product': product,'cartitem':cartitem})

def about(request):
    return render(request,'store/about.html')

def contact(request):
     contact=ContactForm()
     if request.method == "POST":
       form = ContactForm(request.POST)
       if form.is_valid():
            Contact.objects.create(
                name=form.cleaned_data['name'],
                mobile=form.cleaned_data['mobile'],
                email=form.cleaned_data['email'],
                description=form.cleaned_data['message']),
            
            return redirect('store:contact') 
    
     return render(request,'store/contact.html',{'contact':contact})

def cart(request):
    rozarpay_key="rzp_test_7UQe0QqyW56WC6"

    if request.user.is_authenticated:
         carts=Cart.objects.all()

         cartitem=CartItem.objects.filter(user=request.user,cart_id__in=[x.id for x in carts])
         print(cartitem)
         totalcart=CartItem.objects.filter(cart_id__in=[x.id for x in carts],user=request.user)
         totalcartitems=totalcart.aggregate(product_price=Sum('product__price'))
         
         totalgst=totalcartitems.get('product_price') * 18 / 100
         totalsum=totalcartitems.get('product_price')  + totalgst
    else:
         
         
         carts=Cart.objects.get(cart_id=cart_sessions(request))
         cartitem=CartItem.objects.filter(cart_id=carts)
         totalcart=CartItem.objects.filter(cart_id=carts)
         totalcartitems=totalcart.aggregate(product_price=Sum('product__price'))
         
         totalgst=totalcartitems.get('product_price') * 18 / 100
         totalsum=totalcartitems.get('product_price')  + totalgst
    return render(request,'store/cart.html',{'rozarpay_key':rozarpay_key,'cartitem':cartitem,'totalcartitems':totalcartitems,'totalsum':totalsum})

def checkout(request):
    if request.user.is_authenticated:
            rozarpay_key="rzp_test_7UQe0QqyW56WC6"
            currency='INR'
            base_url="http://127.0.0.1:8000"
            callback_url = 'orderreceived/'
            user=User.objects.get(email=request.user)
            carts=Cart.objects.all()
            cartitem=CartItem.objects.filter(user=request.user,cart_id__in=[x.id for x in carts])
          
            totalcart=CartItem.objects.filter(cart_id__in=[x.id for x in carts],user=request.user)
            totalcartitems=totalcart.aggregate(product_price=Sum('product__price'))
                
            totalgst=totalcartitems.get('product_price') * 18 / 100
            totalsum=totalcartitems.get('product_price')  + totalgst
            amount=int(totalsum)
    # else:
    #         rozarpay_key="rzp_test_7UQe0QqyW56WC6"
    #         currency='INR'
    #         base_url="http://127.0.0.1:8000"
    #         callback_url = 'orderreceived/'
    #         user=User.objects.get(email=request.user)
    #         carts=Cart.objects.all()
    #         cartitem=CartItem.objects.filter(user=request.user,cart_id__in=[x.id for x in carts])
    #         print(cartitem)
    #         totalcart=CartItem.objects.filter(cart_id__in=[x.id for x in carts],user=request.user)
    #         totalcartitems=totalcart.aggregate(product_price=Sum('product__price'))
                
    #         totalgst=totalcartitems.get('product_price') * 18 / 100
    #         totalsum=totalcartitems.get('product_price')  + totalgst
    currency="INR"
    try:
                razorpay_order = razorpay_client.order.create(dict(amount=amount*100, currency=currency,payment_capture='0'))
                print('razorpay_order',razorpay_order)
    except BadRequestError as e:
                amount=1.00
                razorpay_order = razorpay_client.order.create(dict( amount=int(amount * 100),   currency='INR', payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    request.session['razorpay_order_id'] = razorpay_order_id
    rozarpay_key=settings.ROZARPAY_KEY
    
    return render(request,'store/checkout.html',{'razorpay_order_id':razorpay_order_id,'rozarpay_key':rozarpay_key,"base_url":base_url,"callback_url":callback_url,'currency':currency,'rozarpay_key':rozarpay_key,'user':user,'cartitem':cartitem,'totalcartitems':totalcartitems,'totalsum':totalsum,'totalgst':totalgst})


def order_confirmation(request):
    return render(request,'store/order-confirmation.html')


def addcart(request):
      
      if request.method == "POST":
            print('okkkk addcart ===========================')
            product_id=request.POST.get('product_id')
            prod=Product.objects.get(id=product_id)
            if request.user.is_authenticated:
            
                cartitem1=CartItem.objects.filter(user=request.user)
                if Cart.objects.filter(cart_id__in=[x.cart for x in cartitem1]).exists():
                    print('okk cartitem')
                    cart1=Cart.objects.filter(cart_id__in=[x.cart for x in cartitem1]).first()
                    CartItem.objects.create(user=request.user,product_id=product_id,cart=cart1,price=prod.price)

                    
            else :
                    
                    if Cart.objects.filter(cart_id=cart_sessions(request)).exists():
                        carts=Cart.objects.get(cart_id=cart_sessions(request))
                        CartItem.objects.create(product_id=product_id,cart=carts,price=prod.price)
                    else:
                        carts=Cart.objects.create(cart_id=cart_sessions(request))
                        CartItem.objects.create(product_id=product_id,cart=carts,price=prod.price)
                            
            return JsonResponse({'msg':'Add to cart'})
      
def order(request):
     email=request.POST.get('email')
     order_id=request.POST.get('order_id')
     price=request.POST.get('amount')
     user1=User.objects.get(email=email)
     Order.objects.create(order_id=order_id,user=user1,total_price=price)

     return JsonResponse({'msg':'okk'})

@csrf_exempt
def rozarpayverify(request):
     if request.method == "POST":
        
      payment_id = request.POST.get('razorpay_payment_id', '')
      razorpay_order_id = request.POST.get('razorpay_order_id', '')
      print('razorpay_order_id',razorpay_order_id)
      signature = request.POST.get('razorpay_signature', '')
     
     
      try:
          params_dict = {  'razorpay_order_id': razorpay_order_id,  'razorpay_payment_id': payment_id,  'razorpay_signature': signature  }
          result = razorpay_client.utility.verify_payment_signature( params_dict)
      except Exception as e:
              print(e)
              return redirect('store:home')
    #   if result is not None:
           
    #        return redirect('store:order_confirmation')

      
      if result is not None:
         allorders=Order.objects.get(order_id=razorpay_order_id)
         carts=CartItem.objects.filter(user__email=allorders.user.email).first()
         cart = Cart.objects.get(cart_id=carts.cart)
         cart.delete()
        #  allorders1=Order.objects.filter(order_id=razorpay_order_id)
        #  total_amount=int(sum(i.total_price for i in allorders1))
        #  amount_gst=total_amount*18/100
        #  amount=int(total_amount+amount_gst)
        #  print('amount',amount)
         
         
     try:
           amount = int(float(allorders.total_price) * 100) 

           print("MOUNT===============",amount)
           am=razorpay_client.payment.capture(payment_id,amount)
           print('am777',am['method'])
           method=am['method']
        #    Util.orderpurchesemail(request,orders,method)
           return redirect('store:order_confirmation')
     except Exception as e:
                    print(e)
                    return render(request, 'webapp/paymentfail.html')
      

  