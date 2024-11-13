from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    HomeView,
    RoomView
    )

app_name = 'posts'

urlpatterns = [
    # Home
    path('', views.home, name='list-posts'),
    path('detail-post/<int:pk>/', views.deltail_post, name='detail-post'),
    path('detail-post/<int:pk>/comment/', views.comment, name='comment'), # xem commennt
    path('search/', views.search_post, name='search_post'),
    path('introduction/', views.introduction, name="introduction"),
    path('contact/', views.send_mail_contact, name="contact"),
    path('notfound/', views.notfound, name="notfound"),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    # path('usersendmail/', views.send_mail_contact, name="send_mail"),
    
    
    
    # User admin xem sửa xóa các sp, trạng thái
    path('admin/', views.dashboard, name='dashboard'),
    path('admin/user-list/', views.user_list, name='list-user'),
    path('admin/orders/', views.order_list, name='list-order'),
    
    # crud post admin
    path('admin/list-posts/', views.adminListPost, name='admin-list-posts'),
    path('admin/update-post/<int:pk>/', views.update_post_view, name='update-post'),
    path('admin/create-post/', views.create_post_view, name='create-post'),
    path('admin/delete-post/<int:pk>/', views.delete_post, name='delete-post'),
     
    # crud category admin
    path('admin/list-category/', views.list_category, name='list-category'),
    path('admin/create-category/',views.create_category_view, name='create-category'),
    path('admin/update-category/<int:pk>/', views.update_category_view, name="update-category"),
        
    # Cart   
    path('list-cart/', views.list_cart, name='list_cart'),  
    path('delete_cart/<int:item_id>/', views.delete_cart, name='delete_cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_all_cart/', views.delete_all_cart ,name='delete_all_cart'),
    path('latest-order/', views.latest_order, name='order_latest'), #user xem đơn hang của họ
    path('checkout/', views.checkout, name='checkout'),
    
    # auth
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    
    # Chat room
    path('room/<str:room_name>/<str:username>/', RoomView, name="room"),
    path('room/default/', HomeView, name="default_room"),
    
    
]