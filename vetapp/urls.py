from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='vetapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('agregar_mascota/', views.agregar_mascota, name='agregar_mascota'),
    path('agregar_ficha/', views.agregar_ficha, name='agregar_ficha'),
    path('ver-cliente/', views.ver_cliente, name='ver_cliente'),
    path('ver_mascotas/', views.ver_mascota, name='ver_mascotas'),
]
