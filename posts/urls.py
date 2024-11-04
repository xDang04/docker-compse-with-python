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
    CreateCategoryView,
    latest_order,
    HomeView,
    RoomView
    )

app_name = 'posts'

urlpatterns = [
    # Home
    path('list-posts/', ListPostView.as_view(), name='list-posts'),
    path('detail-post/<int:pk>/', DetailPostView.as_view(), name='detail-post'),
    path('detail-post/<int:pk>/comment/', views.comment, name='comment'), # xem commennt
    path('search/', views.search_post, name='search_post'),
    path('introduction/', views.introduction, name="introduction"),
    path('contact/', views.contact, name="contact"),
    
    # User admin xem sửa xóa các sp, trạng thái
    path('admin/', views.dashboard, name='dashboard'),
    path('admin/user-list/', views.user_list, name='list-user'),
    path('admin/orders/', views.order_list, name='list-order'),
    
    # crud post admin
    path('admin/list-posts/', views.adminListPost, name='admin-list-posts'),
    path('admin/update-post/<int:pk>/', UpdatePostView.as_view(), name='update-post'),
    path('admin/create-post/', CreatePostView.as_view(), name='create-post'),
    path('admin/delete-post/<int:pk>/', views.delete_post, name='delete-post'),
     
    # crud category admin
    path('admin/list-category/', ListCategoryView.as_view(), name='list-category'),
    path('admin/create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('admin/update-category/<int:pk>/', UpdateCategory.as_view(), name="update-category"),
    
    # Cart   
    path('list-cart/', views.list_cart, name='list_cart'),  
    path('delete_cart/<int:item_id>/', views.delete_cart, name='delete_cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_all_cart/', views.delete_all_cart ,name='delete_all_cart'),
    path('latest-order/', latest_order, name='order_latest'), #user xem đơn hang của họ
    path('checkout/', views.checkout, name='checkout'),
    
    # auth
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    
    # Chat room
    path('room/<str:room_name>/<str:username>/', RoomView, name="room"),
    path('room/default/', HomeView, name="default_room"),
    
    
]