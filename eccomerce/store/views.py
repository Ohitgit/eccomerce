from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.db.models import Sum

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
                    print('okkk')
                    
                    carts = Cart.objects.get(cart_id=cart_sessions(request))
                    print('carts=================', carts)
                    cart_exists = CartItem.objects.filter(cart=carts).exists()
                    if cart_exists:
                        cart_items = CartItem.objects.filter(cart=carts)
                        for item in cart_items:
                            item.user = user
                            item.save()
                except Exception as a:
                     print(a)
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
        cartitem=CartItem.objects.get(product_id=product.id,user=request.user)
    else:
         cart=Cart.objects.all()
         cartitem=CartItem.objects.filter(product_id=product.id,cart_id__in=[x.id for x in cart]).exists()

    return render(request, 'store/products/detail.html', {'product': product,'cartitem':cartitem})

def about(request):
    return render(request,'store/about.html')

def contact(request):
    return render(request,'store/contact.html')

def cart(request):
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
    return render(request,'store/cart.html',{'cartitem':cartitem,'totalcartitems':totalcartitems,'totalsum':totalsum})

def checkout(request):
    return render(request,'store/checkout.html')



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