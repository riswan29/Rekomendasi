from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.contrib import messages
import pickle


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect('login')
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
                    return redirect('formP')
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
    produk_list = Produk.objects.order_by('-id')[:8]
    return render(request, 'user/dash.html',{'produk_list': produk_list})
def anonim(request):
    return render(request, 'user/anon.html')

def produk_list(request):
    produk_list = Produk.objects.all()
    print(produk_list)
    return render(request, 'produk/produk_list.html', {'produk_list': produk_list})

def shop(request):
    produk_shop = Produk.objects.all()
    user = request.user
    # query = request.GET.get('q', '')  # Get search query

    # # Filter products based on the user and search query
    # produk_joined = Produk.objects.filter(
    #     Q(nama_barangicontains=query) | Q(tipe_motoricontains=query) | Q(jenis_ban__icontains=query)
    # )
    # print(produk_joined)
    return render(request, 'produk/shop.html', {'produk_shop': produk_shop})

def produk_detail(request, produk_id):
    produk = get_object_or_404(Produk, pk=produk_id)
    rekomendasi = Produk.objects.order_by('-id')[:4]
    return render(request, 'produk/desk.html', {'produk': produk,
                                                'rekomendasi':rekomendasi,
                                                })

def profile(request):
    user = request.user

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()

            # Jika password baru diisi, perbarui sesi otentikasi
            if form.cleaned_data['new_password']:
                update_session_auth_hash(request, user)

            # Optional: Add a success message
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            # Optional: Add an error message
            messages.error(request, 'Error updating profile. Please check the form.')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'user/profile.html', {'form': form})

@login_required(login_url='login')
def formP(request):
    motor_choices = Produk.motor_choice
    jenis_ban_choices = Produk.BAN_OPSI
    ukuran_choices = Produk.ukuran_choice
    harga_choices = [('1000', '1000'), ('2000', '2000'), ('3000', '3000')]  # Replace this with your actual choices

    context = {
        'motor_choices': motor_choices,
        'jenis_ban_choices': jenis_ban_choices,
        'ukuran_choices': ukuran_choices,
        'harga_choices': harga_choices,
    }

    return render(request, 'user/promp.html', context)

import pandas as pd
from django.shortcuts import render, redirect
from .models import Produk

def tambah_produk_dari_excel(request):
    if request.method == 'POST':
        file_excel = request.FILES['file_excel']

        # Gunakan pandas untuk membaca data dari file Excel
        data_excel = pd.read_excel(file_excel)

        # Iterasi melalui baris Excel dan tambahkan produk ke database
        for index, row in data_excel.iterrows():
            Produk.objects.create(
                nama_barang=row['nama_barang'],
                tipe_motor=row['tipe_motor'],
                jenis_ban=row['jenis_ban'],
                rating=row['rating'],
                ukuran=str(row['ukuran']),
                # harga=row['harga'],
                # deskripsi=row['deskripsi'],
                # Sesuaikan dengan kolom file Excel dan model Anda
            )

        return redirect('daftar_produk')  # Ganti 'daftar_produk' dengan nama URL daftar produk Anda
 # Ganti 'tambah_produk_dari_excel.html' dengan template yang sesuai
#


def get_recommendations(user_id):
    # Load model rekomendasi (misalnya, 'collab1.pkl')
    with open('app\collab1.pkl', 'rb') as file:
        loaded_data_fix = pickle.load(file)

    # Hitung rata-rata prediksi untuk setiap pengguna
    user_avg_ratings = loaded_data_fix.mean(axis=1)

    # Rangking pengguna berdasarkan rata-rata prediksi
    ranked_users = user_avg_ratings.sort_values(ascending=False)

    # Pilih satu pengguna dengan peringkat teratas
    user_idx_to_display = ranked_users.index[0]

    # Rekomendasi Top-N untuk satu pengguna
    top_n_recommendations = loaded_data_fix.loc[user_idx_to_display].sort_values(ascending=False).head(8)

    # Ambil ID produk dari rekomendasi
    recommended_product_ids = top_n_recommendations.index

    return recommended_product_ids

# View untuk menampilkan rekomendasi dan detail produk
def recommendation_view(request):
    # Mendapatkan rekomendasi berdasarkan user ID (gantilah dengan user ID yang sesuai)
    user_id = 122
    recommended_product_ids = get_recommendations(user_id)

    # Mendapatkan objek Produk berdasarkan ID
    recommended_products = Produk.objects.filter(id__in=recommended_product_ids)

    # Render template dengan data produk yang direkomendasikan
    return render(request, 'recommendations.html', {'recommended_products': recommended_products})
