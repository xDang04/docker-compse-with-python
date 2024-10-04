from django.urls import path
from api import views
from api.views import (
    update_post,
    create_post,
    delete_post,
    update_category,
    )

app_name = 'api'


urlpatterns = [
    path('update-post/', update_post, name='api-update-post'),
    path('create-post/', create_post, name='api-create-post'),
    path('delete-post/', delete_post, name='api-delete-post'),
    path('detail-post/', delete_post, name='api-detail-post'),
    path('update-category/', update_category, name='api-update-category'),
]