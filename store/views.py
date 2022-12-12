import datetime
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse
from store.form import RegisterForm
from .models import Customer, Order, OrderItem, Product, Shipping
from django.http import JsonResponse
import json
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.views import LoginView
from django.views.generic import  CreateView
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class Login(LoginView):
    template_name = 'registration/login.html'

def Signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)


        if form.is_valid():
            print('valid')
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password2 = form.cleaned_data['password2']
            
            user = User.objects.create_user(username, email, password2)
            user.save()

            created_user = authenticate(username=username, password=password2)
            login(request, created_user)

            user_model = User.objects.get(username=username)
            
            customer = Customer.objects.create(user=user_model, email=email)
            customer.save()
            
            return redirect('/')

        
    else:
        form = RegisterForm()
    
    context = {
        'form' : form
    }          

    return render(request, 'registration/signup.html', context)


def store(request):

    data = cartData(request)
    cart_items = data['cart_items']

    products = Product.objects.all()
    context={
        'products': products,
        'cart_items': cart_items

    }
    return render(request, 'store.html', context)

def cart(request):

    data = cartData(request)
    cart_items = data['cart_items']
    items = data['items']
    order = data['order']

    context={
        'items':items,
        'order':order,
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)




def checkout(request):

    data = cartData(request)
    cart_items = data['cart_items']
    items = data['items']
    order = data['order']


    context={
        'items':items,
        'order':order,
        'cart_items': cart_items,
    }
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request,data)
    
    total = data['form']['total']
    order.transaction_id = transaction_id
    
    if total:
        order.complete=True
    order.save()

    if order.shipping == True:
        Shipping.objects.create(
        customer = customer,
        order = order,
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        state =data['shipping']['state'],
        zipcode =data['shipping']['zipcode']
    )




    return JsonResponse('Payment was successful', safe=False)
