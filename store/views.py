from django.shortcuts import render





def store(request):
    return render(request, 'store.html')

def cart(request):
    return render(request, 'cart.html')




def checkout(request):
    context = {

    }
    return render(request, 'checkout.html', context)