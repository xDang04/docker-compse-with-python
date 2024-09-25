from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Cart)
admin.site.register(CustomUser)
admin.site.register(CartItem)
