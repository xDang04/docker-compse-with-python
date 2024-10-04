from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    ListPostView,
    ListCategoryView,
    CreatePostView,
    UpdatePostView,
    DetailPostView,
    UpdateCategory,
    latest_order,
    )

app_name = 'posts'

urlpatterns = [
    path('list-posts/', ListPostView.as_view(), name='list-posts'),
    path('list-category/', ListCategoryView.as_view(), name='list-category'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('update-post/<int:pk>/', UpdatePostView.as_view(), name='update-post'),
    path('update-category/<int:pk>/', UpdateCategory.as_view(), name="update-category"),
    path('detail-post/<int:pk>/', DetailPostView.as_view(), name='detail-post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete-post'),  
    path('search/', views.search_post, name='search_post'),
    path('list_cart/', views.list_cart, name='list_cart'),  
    path('delete_cart/<int:item_id>/', views.delete_cart, name='delete_cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_all_cart/', views.delete_all_cart ,name='delete_all_cart'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('latest-order/', latest_order, name='order_latest'),
    path('introduction/', views.introduction, name="introduction"),
    path('contact/', views.contact, name="contact"),
    path('checkout/', views.checkout, name='checkout'),
    # path('order-success/', views.order_success, name='order_success'),
    
    path("chatlobby/", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]