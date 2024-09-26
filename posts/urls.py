from django.urls import path
from . import views
from .views import (
    ListPostView,
    CreatePostView,
    UpdatePostView,
    DetailPostView,
    )

app_name = 'posts'

urlpatterns = [
    path('list-posts/', ListPostView.as_view(), name='list-posts'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('update-post/<int:pk>/', UpdatePostView.as_view(), name='update-post'),
    path('detail-post/<int:pk>/', DetailPostView.as_view(), name='detail-post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete-post'),  
    path('search/', views.search_post, name='search_post'),
     path('delete_cart/<int:item_id>/', views.delete_cart, name='delete_cart'),
      
  
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('list_cart/', views.list_cart, name='list_cart'),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    
    
    path("chatlobby/", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]