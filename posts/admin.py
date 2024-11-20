from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(ChatOneToOne)
admin.site.register(Message)
admin.site.register(Payment_VNPAY)