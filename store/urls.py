from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.updateItem, name='update_item'),
    path('process-order/', views.processOrder, name='process_order'),
    path('signup/', views.Signup , name='signup'),
    path('login/', views.Login.as_view() , name='login'),
    path('logout/', LogoutView.as_view() , name='logout'),
]

