from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            form.save()
            return redirect('login')  # Redirect to a success page
    else:
        form = RegistrationForm()
    return render(request, 'registrasi/registrasi.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('adm')
                else: 
                    return redirect('usr')
            else:
                error_message = "Invalid credentials. Please try again."
                return render(request, 'registrasi/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'registrasi/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def admin_dash(request):
    return render(request, 'admin/dash.html')
def user_dash(request):
    return render(request, 'user/dash.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list')  # Ganti dengan nama URL untuk daftar produk
    else:
        form = ProductForm()
    return render(request, 'produk/tambah_produk.html', {'form': form})

def produk_list(request):
    produk_list = Produk.objects.all()
    
    return render(request, 'produk/produk_list.html', {'produk_list': produk_list})