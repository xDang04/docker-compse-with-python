from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib import messages
import json


# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

class ListPostView(ListView):
    model = Post
    template_name = 'posts/list-posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

class CreatePostView(SuccessMessageMixin, CreateView):
    template_name = 'posts/create-post.html'  
    form_class = CreatePostForm
    success_message = 'Create Post successfully!'
    
class UpdatePostView(SuccessMessageMixin, UpdateView):
    model = Post
    template_name = 'posts/update-post.html'
    fields = ['name', 'content']
    success_message = 'Update Post successfully!'
    
    def get_success_url(self):
        return reverse('posts:list-posts')

class DetailPostView(DetailView):
    model = Post
    template_name = 'posts/detail-post.html'
    # fields = ['name', 'content', 'image']
       
def delete_post(request, pk):
    post = Post.objects.filter(id=pk)
    post.delete()
    context = {
    #   "messages": "Delete Post successfully",
      'posts': Post.objects.all()
    }
    return render(request, 'posts/list-posts.html', context)

def search_post(request):
    query = request.GET.get('query')  # Lấy từ khóa tìm kiếm từ URL
    results = []
    if query:
        # Tìm kiếm trong title hoặc content chứa từ khóa
        results = Post.objects.filter(name__icontains=query)
    # Render the search results in the template
    return render(request, 'posts/search_results.html', {'query': query, 'results': results})

def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Tạo người dùng mới
            messages.success(request, 'Đăng ký thành công!')
            return redirect('posts:list-posts')
        else:
            messages.error(request, 'Đã có lỗi xảy ra. Vui lòng kiểm tra lại.')
    else:
        form = CustomerRegisterForm()
    
    return render(request, 'auth/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Xác thực người dùng
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Đăng nhập người dùng
                messages.success(request, 'Đăng nhập thành công!')
                return redirect('posts:list-posts')  # Chuyển hướng đến danh sách bài viết
            else:
                messages.error(request, 'Tên người dùng hoặc mật khẩu không đúng.')
    else:
        form = CustomerLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})

def add_to_cart(request, pk):
    post = get_object_or_404(Post, id_post=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)  # Tạo giỏ hàng nếu chưa có

    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    cart_item, created = CartItem.objects.get_or_create(cart=cart, post=post)
    if not created:
        cart_item.quantity += 1  # Tăng số lượng nếu sản phẩm đã có trong giỏ hàng
    cart_item.save()

    return redirect('posts:list_cart')  # Redirect đến trang giỏ hàng
def list_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    total_price = 0
    
    if cart:
        items = cart.items.all()
        total_price = sum(item.quantity * item.post.price for item in items)
    else:
        items = []
    
    return render(request, 'cart/list_cart.html', {
        'cart' : cart,
        'items' : items,
        'total_price' : total_price
    })
    
def delete_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    # Delete post cart
    cart_item.delete()  
    return redirect('posts:list_cart')