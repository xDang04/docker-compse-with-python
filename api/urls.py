from django.urls import path
from api import views
from api.views import (
    update_post,
    create_post,
    delete_post,
    update_category,
    delete_category,
    create_category,
    )

app_name = 'api'


urlpatterns = [
    path('update-post/', update_post, name='api-update-post'),
    path('create-post/', create_post, name='api-create-post'),
    path('delete-post/', delete_post, name='api-delete-post'),
    path('update-category/', update_category, name='api-update-category'),
    path('delete-category/', delete_category, name='api-delete-category'),
    path('create-category/', create_category, name='api-create-category'),
]