
from posts.models import Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import json
from posts.models import Category
from django.core import serializers
from posts.models import PostSerializer
from posts.models import CategorySerializer
from rest_framework import status

# Create your views here.
@api_view(["POST"])
def update_post(request):
    try:
        # request.POST.get not input data
        body = request.data
        id_instance = body.get('id_post')
        post = Post.objects.filter(id_post=id_instance).first()
        # Giữ giá trị cũ nếu không có dữ liệu mới
        post.name = body.get('name', post.name)  
        post.price = body.get('price', post.price)
        post.content = body.get('content', post.content)
        post.ingredient = body.get('ingredient', post.ingredient)

        category_id = body.get('category')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)  # Kiểm tra danh mục có tồn tại
                post.category = category
            except Category.DoesNotExist:
                return Response({"error": "Category not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        image = body.get('image')
        if image:
            post.image = image
        post.save()
        data = PostSerializer(post).data
        return Response(data)
    except Exception as e:
        print("Error creating post:", e)
        return Response({"error": "Failed to update post. Please check the input data and try again."},
            status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(["POST"])
def update_category(request):
    try:
        body= request.data
        id_cate = body.get('id')
        if not id_cate:
            return Response({"error": "Category ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.filter(id=id_cate).first()
        
        if category is None:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
            
        category.name = body.get('name', category.name)
        category.save()
        data = CategorySerializer(category).data
        return Response(data, status=status.HTTP_200_OK)
    
    except Category.DoesNotExist:
        return Response({"error": "Category does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        print("Error updating category:", e)
        return Response({"error": "Failed to update category. Please check the input data and try again."},
                        status=status.HTTP_400_BAD_REQUEST)
        
# @api_view(['GET'])
# def get_categories(request):
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     return JsonResponse(serializer.data, safe=False)

@api_view(["POST"])
def create_post(request):
    try:
        body = request.data
        print("Request data:", body)
        name = body.get('name')
        content = body.get('content')
        price = body.get('price')
        ingredient = body.get('ingredient')
        category_id = body.get('category')
        print("cccccccccccccccccc",category_id )
        image = body.get('image')
        if not category_id or not category_id.isdigit():
            return Response({"error": "Invalid category ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        category = Category.objects.get(id=category_id)
        post = Post(name=name, content=content, price=price, ingredient=ingredient, category=category)
        if image:
            post.image = image
        post.save()
        data = PostSerializer(post).data
        return Response(data, status=status.HTTP_201_CREATED)   
    except Exception as e:
        print("Error creating post:", e)
        return Response({"error": "Failed to create post. Please check the input data and try again."}, 
            status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["POST"])
def delete_post(request):
    try:
        # print("222222222")
        body = request.data
        id_instance = body.get('id_post')
        post = Post.objects.filter(id_post=id_instance).first()
        if not post:  # If the post does not exist
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)     
        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# @api_view(["POST"])
# def detail_post(request):
#     body = request.data
#     id_instance = body.get('id')
#     body.get('image')
#     body.get('name')
#     Post.object.filter(id = id_instance).first()
    