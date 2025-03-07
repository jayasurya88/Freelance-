
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
]
