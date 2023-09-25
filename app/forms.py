from .models import *
from django import forms

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = customUser
        fields = ('username', 'email', 'password', 'image',)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['gambar1', 'gambar2', 'rating', 'deskripsi', 'kategori', 'nama_barang',]