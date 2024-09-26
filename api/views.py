
from posts.models import Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.core import serializers
from posts.models import PostSerializer
from rest_framework import status

# Create your views here.
@api_view(["POST"])
def update_post(request):
    try:
        # request.POST.get not input data
        body = request.data
        id_instance = body.get('id_post')
        # print("-----------")
        content = body.get('content')
        name = body.get('name')
        price = body.get('price')
        image = body.get('image')        
        post = Post.objects.filter(id_post=id_instance).first()
        # print("post-----------------", id_instance)
        post.name = name
        post.price = price
        post.content = content
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
def create_post(request):
    try:
        body = request.data
        name = body.get('name')
        content = body.get('content')
        price = body.get('price')
        image = body.get('image')
        post = Post(name=name, content=content, price=price)
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
    