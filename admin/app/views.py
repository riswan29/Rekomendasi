from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin:index')
                else: 
                    return redirect('dashboard')
            else:
                error_message = "Invalid credentials. Please try again."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
