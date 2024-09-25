
from django import forms
from .models import *
from django.core.exceptions import ValidationError

class CreatePostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['id_post', 'name', 'content', 'image']
    
class CartItemForm(forms.ModelForm):
  class Meta:
    model = CartItem
    fields = ['quantity']
    
class CustomerRegisterForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

  class Meta:
    model = CustomUser
    fields = ['username', 'email', 'password']

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get("password")
    confirm_password = cleaned_data.get("confirm_password")

    if password != confirm_password:
      raise ValidationError("Confirm Password is incorrect")
    
class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
# class SearchForm(forms.Form):
#   query = forms.CharField(label='Search Keywords', max_length=100)