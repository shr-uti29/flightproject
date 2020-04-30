from django.urls import path

from . import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('main',views.main,name='main'),
    path('logout',views.logout,name='logout'),
    path('edit',views.edit,name='edit'),
    path('book',views.book,name='book'),
    path('availability/<str:fr>/<str:to>/<str:dt>/<str:dt1>',views.availability,name='availability'),
    path('availability_one/<str:fr>/<str:to>/<str:dt>',views.availability_one,name='availability_one'),
    path('mybookings',views.mybookings,name='mybookings'),
    path('change_password',views.change_password,name='change_password'),
    path('seat',views.seat,name='seat'),
    path('seat_ret',views.seat_ret,name='seat_ret'),
    path('payment',views.payment,name='payment'),
]