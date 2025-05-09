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
    path('fichas/', views.ver_ficha, name='ver_ficha'),
    path('ficha/agregar/', views.agregar_ficha, name='agregar_ficha'),
    path('ajax/obtener-cliente/', views.obtener_cliente_por_mascota, name='obtener_cliente'),
    path('ultimas_fichas/', views.ultimas_10_fichas, name='ultimas_fichas'),
    path('detalle_ficha/<int:id_ficha>/', views.ver_detalle_ficha, name='ver_detalle_ficha'),
    path('mascota/<int:id_mascota>/fichas/', views.ver_fichas_mascota, name='ver_fichas_mascota'),
    # Modificar la ruta para que reciba un parámetro id_mascota
    path('ver_mascota/<int:id_mascota>/', views.ver_mascota, name='ver_mascota'),
    path('editar_mascota/<int:id_mascota>/', views.editar_mascota, name='editar_mascota'),
    path('editar_cliente/<int:id_cliente>/', views.editar_cliente, name='editar_cliente'),
    path('editar_ficha/<int:id_ficha>/', views.editar_ficha, name='editar_ficha'),
    path('graficos/', views.graficos, name='graficos'),
    
    
    

]
