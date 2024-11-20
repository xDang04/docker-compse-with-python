"""
URL configuration for Django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls', namespace='posts')),
    path('api/', include('api.urls', namespace='api')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('indexpay/', views.index, name='index'),
    path('payment', views.payment, name='payment'),
    path('payment_ipn', views.payment_ipn, name='payment_ipn'),
    path('payment_return', views.payment_return, name='payment_return'),
    path('query', views.query, name='query'),
    path('refund', views.refund, name='refund'),
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
