import json
from .models import Order, OrderItem, Product, Shipping, Customer

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        print(cart)
    except:
        cart = {}
    
    items = []
    order = {'get_cart_total':0, 'get_item_total':0, 'shipping': True}
    cart_items = order['get_item_total']

    for i in cart:
        try:
            cart_items += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']
            order['get_cart_total'] += total
            order['get_item_total'] += cart[i]['quantity']

            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageUrl': product.imageUrl
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] == True

        except:
            pass
    return {'cart_items': cart_items, 'order':order, 'items':items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        items = order.items.all()
        cart_items = order.get_item_total
    else:
        cookieData = cookieCart(request)
        cart_items = cookieData['cart_items']
        items = cookieData['items']
        order = cookieData['order']

    return {'cart_items': cart_items, 'order':order, 'items':items}

def guestOrder(request, data):
    print('User is not logged in.')
    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
        email = email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete = False
        )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderitem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity= item['quantity']
        )

    return customer, order