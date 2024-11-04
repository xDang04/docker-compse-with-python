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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.

class ListPostView(ListView):
    model = Post
    template_name = 'users/posts/list-posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

@login_required  
def adminListPost(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, "admin/posts/list-post.html", context)


class ListCategoryView(ListView):
    model = Category
    template_name = 'admin/category/list-category.html'
    context_object_name = 'categories'
    paginate_by = 2

class CreatePostView(SuccessMessageMixin, CreateView):
    model = Post
    template_name = 'admin/posts/create-post.html'  
    form_class = CreatePostForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Lấy danh sách category
        return context
    
    # success_message = 'Create Post successfully!'

class CreateCategoryView(SuccessMessageMixin, CreateView):
    model = Category
    template_name = 'admin/category/add-category.html'  
    form_class = CreateCategoryForm 

class UpdatePostView(SuccessMessageMixin, UpdateView):
    model = Post
    template_name = 'admin/posts/update-post.html'
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
    template_name = 'admin/category/update-category.html'
    fields = '__all__'
    def get_success_url(self):
        return reverse('posts:list-category')

class DetailPostView(DetailView):
    model = Post
    template_name = 'users/posts/detail-post.html'
    # fields = ['name', 'content', 'image']

@login_required       
def delete_post(request, pk):
    post = Post.objects.filter(id=pk)
    post.delete()
    context = {
      'posts': Post.objects.all()
    }
    return render(request, 'admin/posts/list-posts.html', context)

@login_required
def search_post(request):
    query = request.GET.get('query')  # Lấy từ khóa tìm kiếm từ URL
    results = []
    if query:
        # Tìm kiếm name chứa từ khóa
        results = Post.objects.filter(name__icontains=query)
    # Render the search results in the template
    return render(request, 'users/posts/search_results.html', {'query': query, 'results': results})

@login_required
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

    return render(request, 'users/cart/list_cart.html', {
        'cart': cart,
        'items': item_totals,
        'total_price': total_price
    })
    
@login_required   
def delete_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    # Delete post cart
    cart_item.delete()  
    return redirect('posts:list_cart')
 
@login_required
def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.")
        return redirect('users/posts/login') 
    
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
    
    return render(request, 'admin/auth/signup.html', {'form': form})


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
    
    return render(request, 'admin/auth/login.html', {'form': form})

@login_required
def introduction(request):
    return render(request, "users/posts/introduction.html")

@login_required
def contact(request):
    return render(request, "users/posts/contact.html")

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, "Giỏ hàng của bạn đang trống!")
        return redirect('posts:checkout')

    if request.method == 'POST':
        address = request.POST.get('address')  
        phone = request.POST.get('phone')

        if not address:  
            messages.error(request, "Địa chỉ không được để trống!")
            return redirect('posts:checkout')

        total = sum(item.quantity * item.post.price for item in cart.items.all())
        order = Order.objects.create(
            user=request.user,
            address=address,
            phone=phone,
            total=total,
            status='Chờ xác nhận'
        )
        
        cart.items.all().delete()
        cart.delete()
        messages.success(request, "Đơn hàng của bạn đã được xác nhận!")
        return redirect('posts:order_latest') 

    context = {
        'cart': cart,
    }
    return render(request, 'users/cart/checkout.html', context)
  
@login_required      
def delete_all_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user)
        cart.delete()
        return redirect('posts:list-posts')

@login_required
def latest_order(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')

    # Prepare the context with the orders data
    context = {
        'orders': orders,
    }
        
    return render(request, 'users/cart/latest_order.html', context)

@login_required
def order_list(request):
    # Nếu là yêu cầu POST, xử lý cập nhật trạng thái đơn hàng
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        try:
            # Lấy đơn hàng dựa trên order_id
            order = Order.objects.get(id=order_id)
            # Cập nhật trạng thái mới
            order.status = new_status
            order.save()  # Lưu thay đổi vào cơ sở dữ liệu
            messages.success(request, f"Đã cập nhật trạng thái đơn hàng {order_id} thành '{new_status}'")
        except Order.DoesNotExist:
            messages.error(request, "Đơn hàng không tồn tại.")

        # Redirect về lại trang danh sách đơn hàng
        return redirect('posts:list-order')

    # Lấy tất cả đơn hàng để hiển thị trên trang
    orders = Order.objects.all()
    paginator = Paginator(orders , 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'users/cart/list-order.html', context)

@login_required
def HomeView(request):
    print("request```````````", request.user)
    if request.method == 'POST':
        username = request.user
        room = request.POST.get('room', 'ManchesterUnited')  # Mặc định là "mu"

        try:
            existing_room = Room.objects.get(room_name__icontains=room)
        except Room.DoesNotExist:
            existing_room = Room.objects.create(room_name=room)
        
        return redirect('posts:room', room_name=existing_room.room_name, username=username)
    
    # Khi là GET request, chuyển hướng đến phòng chat mặc định
    return redirect('posts:room', room_name='ManchesterUnited', username=request.user)

@login_required  
def RoomView(request, room_name, username):
    existing_room = Room.objects.get(room_name__icontains=room_name)
    get_messages = Message.objects.filter(room=existing_room)
    context={
        'messages' : get_messages,
        'username' : username,
        'room_name' : existing_room.room_name,
    }
    
    return render(request, "chat/room.html", context)


@login_required
def comment(request,pk):
    post = get_object_or_404(Post, id_post=pk)
    comments = post.comments.all()
    print("coment--------------",comments)
    print("id--------------",pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            print(f'New comment saved: {new_comment.content}')
            return redirect('posts:comment', pk=post.id_post)
        else:
            print('Form is not valid')
    else:
        form = CommentForm()
    return render(request, 'users/posts/comment.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def dashboard(request):
    return render(request, "admin/dashboard/chart.html")


@login_required
def user_list(request):
    users = User.objects.filter() #is_superuser=False
    paginator = Paginator(users, 5)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'admin/auth/list-user.html', context)

