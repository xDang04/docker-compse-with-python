from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib import messages



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

class ListCategoryView(ListView):
    model = Category
    template_name = 'category/list-category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CreatePostView(SuccessMessageMixin, CreateView):
    model = Post
    template_name = 'posts/create-post.html'  
    form_class = CreatePostForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Lấy danh sách category
        return context
    
    success_message = 'Create Post successfully!'
    
class UpdatePostView(SuccessMessageMixin, UpdateView):
    model = Post
    template_name = 'posts/update-post.html'
    fields = ['name', 'content', 'ingredient']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        return context
    success_message = 'Update Post successfully!'
    
    def get_success_url(self):
        return reverse('posts:list-posts')

class UpdateCategory(UpdateView):
    model = Category
    template_name = 'category/update-category.html'
    fields = '__all__'
    def get_success_url(self):
        return reverse('posts:list-category')

class DetailPostView(DetailView):
    model = Post
    template_name = 'posts/detail-post.html'
    # fields = ['name', 'content', 'image']
       
def delete_post(request, pk):
    post = Post.objects.filter(id=pk)
    post.delete()
    context = {
      'posts': Post.objects.all()
    }
    return render(request, 'posts/list-posts.html', context)

def search_post(request):
    query = request.GET.get('query')  # Lấy từ khóa tìm kiếm từ URL
    results = []
    if query:
        # Tìm kiếm name chứa từ khóa
        results = Post.objects.filter(name__icontains=query)
    # Render the search results in the template
    return render(request, 'posts/search_results.html', {'query': query, 'results': results})

def list_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    total_price = 0
    item_totals = []

    if cart:
        items = cart.items.all()  # Sử dụng related_name 'items'
        for item in items:
            item_total = item.quantity * item.post.price
            item_totals.append((item, item_total))
            total_price += item_total
    else:
        items = []

    return render(request, 'cart/list_cart.html', {
        'cart': cart,
        'items': item_totals,
        'total_price': total_price
    })
    
def delete_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    # Delete post cart
    cart_item.delete()  
    return redirect('posts:list_cart')
 

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.")
        return redirect('/posts/login') 
    
    post = get_object_or_404(Post, id_post=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart, created = Cart.objects.get_or_create(user=request.user) 

    cart_item, created = CartItem.objects.get_or_create(cart=cart, post=post)
    if not created:
        cart_item.quantity += 1 
    else:
        cart_item.quantity = quantity
    cart_item.save()
    
    
    return redirect('posts:list_cart') 


def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Tạo người dùng mới
            messages.success(request, 'Đăng ký thành công!')
            return redirect('posts:login')
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

def introduction(request):
    return render(request, "posts/introduction.html")

def contact(request):
    return render(request, "posts/contact.html")

def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')  
        phone = request.POST.get('phone')

        if not address:  
            messages.error(request, "Địa chỉ không được để trống!")
            return redirect('posts:checkout')

        cart = Cart.objects.filter(user=request.user).first()
        if cart and cart.items.exists():
            total = sum(item.quantity * item.post.price for item in cart.items.all()) 
            order = Order.objects.create(
                user=request.user,
                address=address,
                phone=phone,
                total=total,
                status='Chờ xác nhận'
            )
            # for cart_item in cart.items.all():
            #     CartItem.objects.create(
            #         cart=cart,  # Liên kết với cart hiện tại
            #         post=cart_item.post,
            #         quantity=cart_item.quantity,
            #         order=order
            #     )
            
            cart.items.all().delete()
            cart.delete()
            messages.success(request, "Đơn hàng của bạn đã được xác nhận!")
            
            return redirect('posts:order_latest') 
        else:
            messages.error(request, "Giỏ hàng của bạn đang trống!")
    return render(request, 'cart/checkout.html')
        
def delete_all_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user)
        cart.delete()
        return redirect('posts:list-posts')
    
    
def latest_order(request):
    latest_order = Order.objects.filter(user=request.user).order_by('-order_date').first()
    # latest_order = get_object_or_404(Order, user=request.user)
    # order_items = CartItem.objects.filter(order=latest_order)
    
    if latest_order:
        context = {
            # 'order_id': latest_order.id,
            'status': latest_order.status,
            'order_date': latest_order.order_date,
            'total': latest_order.total,
            'phone' : latest_order.phone,
            'address' : latest_order.address,
            'username': latest_order.user.username,
            'email': latest_order.user.email,
            # 'order_items': order_items,
        }
    else:
        context = {
            'error': 'Không có đơn hàng nào'
        }
        
    return render(request, 'cart/latest_order.html', context)