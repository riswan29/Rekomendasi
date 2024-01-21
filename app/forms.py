from .models import *
from django import forms
from django.contrib.auth.forms import UserChangeForm
#  address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control resume', 'placeholder': 'Jl. xxxxx', 'rows' :'5'}),
class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'type':'email', 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password','placeholder':'Password'}))
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
        fields = ['gambar1', 'rating', 'deskripsi', 'harga', 'nama_barang','tipe_motor', 'tipe_motor']

class CustomUserChangeForm(UserChangeForm):
    new_password = forms.CharField(
        label='Password Baru',
        widget=forms.PasswordInput,
        required=False,
        help_text='Isi hanya jika Anda ingin mengganti password.'
    )

    class Meta:
        model = customUser
        fields = ('full_name', 'password', 'new_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].label = 'Nama'
        self.fields['password'].help_text = 'Password saat ini.'
        self.fields['password'].widget.attrs['autocomplete'] = 'current-password'
        self.fields['new_password'].help_text = 'Isi hanya jika Anda ingin mengganti password.'

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            # Jika password baru diisi, atur password dengan hash
            self.instance.set_password(new_password)
        return new_password
