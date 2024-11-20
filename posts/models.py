from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.hashers import make_password

class Category(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    
    def __str__(self):
        return str(self.name)
class Post(models.Model):
    id_post = models.AutoField(primary_key=True)
    name = models.CharField(max_length=224, null=False, blank=False)
    content = models.TextField(max_length=254, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredient = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id_post)
    
    def get_absolute_url(self):
        return reverse('posts:list-posts', kwargs={})
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart for {self.user.username}'
    
class CartItem(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey('Order', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.quantity} of {self.post.name}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('Chờ xác nhận', 'Chờ xác nhận'),
        ('Chờ giao hàng', 'Chờ giao hàng'),
        ('Đang giao hàng', 'Đang giao hàng'),
        ('Đã nhận hàng', 'Đã nhận hàng'),
        ('Đã hủy', 'Đã hủy'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    order_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f'Order {self.id} - {self.status}'
   
   
class Payment_VNPAY(models.Model):
    order_id = models.BigIntegerField(default=0, blank=True, null=True) 
    amount = models.FloatField(default=0.0, blank=True, null=True)
    order_desc = models.CharField(max_length=200, blank=True, null=True)
    vnp_TransactionNo = models.CharField(max_length=200, null=True, blank=True)
    vnp_ResponseCode = models.CharField(max_length=200, null=True, blank=True)
# class Room(models.Model):
#     room_name = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.room_name
class ChatOneToOne(models.Model):
    user1 = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"
class Message(models.Model):
    chat = models.ForeignKey(ChatOneToOne, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}..."
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"comment by {self.user.username} on {self.post.name}"
   
class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    phone = models.CharField(max_length=15,blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.username
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Ví dụ: Admin, Editor, User
    description = models.TextField(blank=True, null=True)  # Mô tả vai trò

    def __str__(self):  
        return self.name

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'