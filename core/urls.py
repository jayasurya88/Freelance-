
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('account_selection',views.account_selection,name="account_selection"),
    path('login',views.login_view,name="login_view"),
    path('register',views.register,name="register"),
    path('home',views.home,name="home"),
    path('freelance',views.freelance_dashboard,name="freelance_dashboard"),
    path('client',views.client_dashboard,name="client_dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile_view'),
     path('profile/edit/', views.edit_profile, name='edit_profile'),
 path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    
]
