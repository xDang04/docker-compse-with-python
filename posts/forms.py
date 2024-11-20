from django import forms
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError

class CreatePostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['id_post', 'name', 'content', 'image']
  
class CreateCategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ['name']
class CartItemForm(forms.ModelForm):
  class Meta:
    model = CartItem
    fields = ['quantity']
    
class CustomerRegisterForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']


  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get("password")
    confirm_password = cleaned_data.get("confirm_password")

    # Kiểm tra xem mật khẩu và mật khẩu xác nhận có khớp nhau không
    if password and confirm_password and password != confirm_password:
        raise ValidationError("Confirm Password is incorrect")
    return cleaned_data
  
  
  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data["password"])  # Mã hóa mật khẩu
    if commit:
        user.save()  # Lưu người dùng
    return user
      
class UserFormProfile(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name']
class ImageUserForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['phone', 'address', 'profile_image']
class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content']
    widgets = {
      'content': forms.Textarea(attrs={'rows': 4 , 'cols': 90}),
    }
    
class PaymentForm(forms.Form):

    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)