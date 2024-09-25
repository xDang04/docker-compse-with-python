# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.hashers import make_password

class Post(models.Model):
    id_post = models.AutoField(primary_key=True)
    name = models.CharField(max_length=224, null=False, blank=False)
    content = models.TextField(max_length=254, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id_post)
    
    def get_absolute_url(self):
        return reverse('posts:list-posts', kwargs={})

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if not self.pk:  # Chỉ mã hóa mật khẩu khi tạo mới
            self.password = make_password(self.password)  # Mã hóa mật khẩu trước khi lưu
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart for {self.user.username}'
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.post.name}'

    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'