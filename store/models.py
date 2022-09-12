from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    digital = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url=''
        return url
        

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255)

    def get_cart_total(self):
        orderitems = self.items.all()
        total = 0

        for item in orderitems:
            total += item.get_total

        return total
    
    def get_item_total(self):
        orderitems = self.items.all()
        total = 0

        for item in orderitems:
            total += item.quantity

        return total
    
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # to get all the order item that has this order as a parent name set the related_name
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='items', null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    def __str__(self):
        return str(self.product.name)


class Shipping(models.Model):
     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
     address = models.CharField(max_length=200)
     city = models.CharField(max_length=200)
     state = models.CharField(max_length=200)
     zipcode = models.CharField(max_length=255)
     date_added = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return str(self.address)





    
