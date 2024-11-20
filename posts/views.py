import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import random
import requests
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from functools import wraps
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
# Create your views here.

from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
# from django.utils.http import urlquote
from posts.vnpay import vnpay




def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.user.user_role.role.name if hasattr(request.user, 'user_role') else None
            if user_role != role_name:
                return redirect('posts:notfound')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def home(request):
    posts = Post.objects.all()
    
    return render(request, "users/posts/home.html", {
        'posts' : posts,
    })

@role_required('Admin')
def adminListPost(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, "admin/posts/list-post.html", context)

@role_required('Admin')
def list_category(request):
    category = Category.objects.all()
    paginator = Paginator(category, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj' : page_obj
    }
    
    return render(request, "admin/category/list-category.html", context)

@role_required('Admin')
def create_post_view(request):
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     content = request.POST.get('content')
    #     price = request.POST.get('price')
    #     ingredient = request.POST.get('ingredient')
    #     category_id = request.POST.get('category')
    #     image = request.FILES.get('image')  # Lấy ảnh tải lên từ form
        
    #     # Kiểm tra các trường bắt buộc
    #     if not name or not content or not price or not ingredient or not category_id:
    #         messages.error(request, "Vui lòng điền đầy đủ thông tin!")
    #     else:
    #         # Lấy category từ ID được truyền lên
    #         category = Category.objects.get(id=category_id)
    #         # Tạo bài viết mới với các thông tin từ form
    #         post = Post.objects.create(
    #             name=name,
    #             content=content,
    #             price=price,
    #             ingredient=ingredient,
    #             category=category,
    #             image=image
    #         )
    #         messages.success(request, "Bài viết đã được tạo thành công!")
    #         return redirect('posts:admin-list-posts')
    # Lấy danh sách category để hiển thị trong form
    categories = Category.objects.all()

    return render(request, 'admin/posts/create-post.html', {
        'categories': categories,
    })

@role_required('Admin')
def create_category_view(request):
    return render(request, 'admin/category/add-category.html')

@role_required('Admin')
def update_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()
    
    return render(request, "admin/posts/update-post.html", {
        'categories' : categories,
        'post': post,
    })
   
@role_required('Admin') 
def update_category_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, "admin/category/update-category.html", {
        'category' : category,
    })

def deltail_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'users/posts/detail-post.html', {
        'posts' : post,
    })

@role_required('Admin')
def delete_post(request, pk):
    post = Post.objects.filter(id=pk)
    post.delete()
    context = {
      'posts': Post.objects.all()
    }
    return render(request, 'admin/posts/list-posts.html', context)

def search_post(request):
    query = request.GET.get('query')  # Lấy từ khóa tìm kiếm từ URL
    results = []
    if query:
        # Tìm kiếm name chứa từ khóa
        results = Post.objects.filter(name__icontains=query)
    # Render the search results in the template
    return render(request, 'users/posts/search_results.html', {'query': query, 'results': results})

def list_cart(request):
    if not request.user.is_authenticated:
        return render(request, 'users/cart/list_cart.html', {
            'cart': None,
            'items': [],
            'total_price': 0,
            
        })
    
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
    
def delete_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    # Delete post cart
    cart_item.delete()  
    return redirect('posts:list_cart')
 
def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.")
        return redirect('posts:detail-post', pk=pk) 
    
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
                # print("dasssssssssss",user )
                # Kiểm tra role_id của người dùng
                user_role = UserRole.objects.filter(user=user).first()
                role_id = user_role.role_id if user_role else None
                
                # Chuyển hướng dựa trên role_id
                if role_id == 1:
                    return redirect('posts:dashboard')  # Chuyển hướng đến trang dashboard
                # elif role_id == 2:
                #     return redirect('posts:list-posts')  # Chuyển hướng đến danh sách bài viết
                else:
                    return redirect('posts:list-posts')
                    # messages.error(request, 'Không xác định được quyền truy cập.')
            else:
                messages.error(request, 'Tên người dùng hoặc mật khẩu không đúng.')
    else:
        form = CustomerLoginForm()
    
    return render(request, 'admin/auth/login.html', {'form': form})

def introduction(request):
    return render(request, "users/posts/introduction.html")

def view_profile(request):
    return render(request, "admin/auth/profile.html")

def profile_update(request):
    user = request.user
    image_user = UserImage.objects.filter(user=user).first()
    
    if request.method == 'POST':
        profile_form = UserFormProfile(request.POST, instance=user)
        image_form = ImageUserForm(request.POST, request.FILES, instance=image_user)
        
        if profile_form.is_valid() and image_form.is_valid():
            profile_form.save()
            
            if not image_user:
                image_user = UserImage(user=user)
            image_form.instance.user = user
            image_form.save()
            
            return redirect('posts:view_profile')
    else:
        profile_form = UserFormProfile(instance=user)
        image_form = ImageUserForm(instance=image_user)
    
    return render(request, 'admin/auth/profile.html', {
        'profile_form': profile_form,
        'image_form': image_form,
        'user': user,
        'image_user': image_user
    })

# @login_required
# def checkout(request):
#     cart = Cart.objects.filter(user=request.user).first()
#     if not cart or not cart.items.exists():
#         messages.error(request, "Giỏ hàng của bạn đang trống!")
#         return redirect('posts:checkout')

#     total = sum(item.quantity * item.post.price for item in cart.items.all())
    
#     if request.method == 'POST':
#         address = request.POST.get('address')  
#         phone = request.POST.get('phone')

#         if not address:  
#             messages.error(request, "Địa chỉ không được để trống!")
#             return redirect('posts:checkout')

        
#         order = Order.objects.create(
#             user=request.user,
#             address=address,
#             phone=phone,
#             total=total,
#             status='Chờ xác nhận'
#         )
        
#         cart.items.all().delete()
#         cart.delete()
#         # messages.success(request, "Đơn hàng của bạn đã được xác nhận!")
#         return redirect('posts:order_latest') 

#     context = {
#         'cart': cart,
#         'total': total,
#     }
#     return render(request, 'users/cart/checkout.html', context)
  
def delete_all_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user)
        cart.delete()
        return redirect('posts:list_cart')

def latest_order(request):
    if not request.user.is_authenticated:
        
        return render(request, 'users/cart/latest_order.html')
    orders = Order.objects.filter(user=request.user).order_by('-order_date')

    # Prepare the context with the orders data
    context = {
        'orders': orders,
    }
        
    return render(request, 'users/cart/latest_order.html', context)

@role_required('Admin')
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

def HomeView(request):
    if not request.user.is_authenticated:
        return redirect('posts:login')
    
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

def comment(request,pk):
    post = get_object_or_404(Post, id_post=pk)
    comments = post.comments.all()
    # print("coment--------------",comments)
    # print("id--------------",pk)
    
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

@role_required('Admin')
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('posts:login')
    
    return render(request, "admin/dashboard/chart.html")

@role_required('Admin')
def user_list(request):
    users = User.objects.filter() #is_superuser=False
    paginator = Paginator(users, 5)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'admin/auth/list-user.html', context)

def notfound(request):
    return render(request,'users/notfound.html')

def send_mail_contact(request):
    context = {}
    
    if request.method == 'POST':
        your_subject = request.POST.get('your_subject')
        email = request.POST.get('your_email')
        
        message_content = request.POST.get('your_message')
        
        if your_subject and email and message_content:
            try:
                send_mail(your_subject,message_content, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'
    return render(request, "users/posts/contact.html", context)

def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Tìm cuộc trò chuyện giữa hai người dùng, nếu có nhiều phòng, chỉ lấy phòng đầu tiên
    chat = ChatOneToOne.objects.filter(
        (Q(user1=request.user) & Q(user2=other_user)) |
        (Q(user1=other_user) & Q(user2=request.user))
    ).first()

    # Nếu không tồn tại cuộc trò chuyện nào, tạo một cuộc trò chuyện mới
    if not chat:
        chat = ChatOneToOne.objects.create(user1=request.user, user2=other_user)

    # Lấy tất cả tin nhắn trong cuộc trò chuyện
    messages = chat.messages.all().order_by('time_stamp')

    return render(request, 'chat/chat_room.html', {
        'chat_id': chat.id,
        'other_user': other_user,
        'user': request.user,
        'messages': messages,
    })  
  
@role_required('Admin')  
def chatadmin(request,):
    user = request.user
    image_user = UserImage.objects.filter(user=user).first()
    current_user_id = request.user.id
    admin_role = Role.objects.get(name="Admin")
    users = User.objects.exclude(id=current_user_id).exclude(user_role__role=admin_role)
    context = {
        'users': users,
        'current_user_id': current_user_id,
        'user':user,
        'image_user':image_user
    }
    return render(request, 'chat/chatwithuser.html',context)

def index(request):
    return render(request, "index.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment(request):

    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            ipaddr = get_client_ip(request)
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render(request, "vnpay/payment.html", {"title": "Thanh toán"})


def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result


def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        
        payment = Payment_VNPAY.objects.create(
            order_id = order_id,
            amount = amount,
            order_desc = order_desc,
            vnp_TransactionNo = vnp_TransactionNo,
            vnp_ResponseCode = vnp_ResponseCode
        )
        
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return render(request, "vnpay/payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Thành công", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
            else:
                return render(request, "vnpay/payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Lỗi", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
        else:
            return render(request, "vnpay/payment_return.html",
                          {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
    else:
        return render(request, "vnpay/payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

n = random.randint(10**11, 10**12 - 1)
n_str = str(n)
while len(n_str) < 12:
    n_str = '0' + n_str


def query(request):
    if request.method == 'GET':
        return render(request, "vnpay/query.html", {"title": "Kiểm tra kết quả giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_Version = '2.1.0'

    vnp_RequestId = n_str
    vnp_Command = 'querydr'
    vnp_TxnRef = request.POST['order_id']
    vnp_OrderInfo = 'kiem tra gd'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode,
        vnp_TxnRef, vnp_TransactionDate, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "vnpay/query.html", {"title": "Kiểm tra kết quả giao dịch", "response_json": response_json})

def refund(request):
    if request.method == 'GET':
        return render(request, "vnpay/refund.html", {"title": "Hoàn tiền giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_RequestId = n_str
    vnp_Version = '2.1.0'
    vnp_Command = 'refund'
    vnp_TransactionType = request.POST['TransactionType']
    vnp_TxnRef = request.POST['order_id']
    vnp_Amount = request.POST['amount']
    vnp_OrderInfo = request.POST['order_desc']
    vnp_TransactionNo = '0'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_CreateBy = 'user01'
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode, vnp_TransactionType, vnp_TxnRef,
        vnp_Amount, vnp_TransactionNo, vnp_TransactionDate, vnp_CreateBy, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_Amount": vnp_Amount,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_TransactionType": vnp_TransactionType,
        "vnp_TransactionNo": vnp_TransactionNo,
        "vnp_CreateBy": vnp_CreateBy,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "vnpay/refund.html", {"title": "Kết quả hoàn tiền giao dịch", "response_json": response_json})