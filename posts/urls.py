from django.urls import path
from . import views
from .views import (
    ListPostView,
    CreatePostView,
    UpdatePostView,
    DetailPostView, 
    add_to_cart,
    register,
    user_login,
    )

app_name = 'posts'

urlpatterns = [
    path('list-posts/', ListPostView.as_view(), name='list-posts'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('update-post/<int:pk>/', UpdatePostView.as_view(), name='update-post'),
    path('detail-post/<int:pk>/', DetailPostView.as_view(), name='detail-post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete-post'),  
    path('search/', views.search_post, name='search_post'),
      
  
    
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    
    
    path("chatlobby/", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]