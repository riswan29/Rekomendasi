from .models import *
from django import forms
#  address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control resume', 'placeholder': 'Jl. xxxxx', 'rows' :'5'}),
class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'type':'email', 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password','placeholder':'Password'}))
    # image = forms.FileField(widget=forms.FileInput(attrs={'type':'file','class':'form-controll'}))
    image = forms.FileField(widget=forms.FileInput(attrs={'type':'file','class':'form-controll'}))

    class Meta:
        model = customUser
        fields = ('username', 'email', 'password', 'image',)

class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password', 'placeholder': 'Password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'type':'email', 'placeholder':'Email'}))
    class Meta:
        email = forms.EmailField()
        password = forms.CharField(widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['gambar1', 'gambar2', 'rating', 'deskripsi', 'kategori', 'nama_barang',]
