from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
   
    path('', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('find_bus',views.find_bus,name="find_bus"),
    path('payment/', views.payment, name='payment'),
    path('payment/<int:town_id>/', views.bus_payment, name='bus_payment'), 
    path('confirm-payment/<int:town_id>/', views.confirm_payment, name='confirm_payment'),
    path('logout/', views.logout_view, name='logout'),
    path('clerk/dashboard/', views.clerk_dashboard, name='clerk_dashboard'),
    path('after-login/', views.after_login_redirect, name='after_login_redirect'),
]

