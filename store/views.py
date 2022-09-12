from django.shortcuts import render
from .models import Order, OrderItem, Product

def store(request):
    products = Product.objects.all()
    context={
        'products': products
    }
    return render(request, 'store.html', context)

def cart(request):
    #this view dynamically renders the item stored in our cart

    if request.user.is_authenticated:
        customer = request.user.customer
        
        #get the order if exist, created for this currently logged in user
        #create if it does not exist
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        '''
        gets all the orderitems whose parent is the order created by this specific customer
        i.e gets all orderitems that falls under or that is a child of this order
        A.K.A reverse lookup
        '''

        items = order.items.all()
        print(items)

    else:
        items = []
        order = {'get_cart_total':0, 'get_item_total':0}

    context={
        'items':items,
        'order':order
    }
    return render(request, 'cart.html', context)




def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        items = order.items.all()

    else:
        items = []
        order = {'get_cart_total':0, 'get_item_total':0}

    context={
        'items':items,
        'order':order
    }
    return render(request, 'checkout.html', context)