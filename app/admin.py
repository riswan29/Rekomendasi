from django.contrib import admin
from .models import *


class tableUser(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'is_staff', 'is_active','image',]
    fields = ['image']
admin.site.register(customUser, tableUser)


class tableProduk(admin.ModelAdmin):
    list_display = [ 'nama_barang', 'tipe_motor']
    field = ['nama_barang']
admin.site.register(Produk, tableProduk)

class tableSCORE(admin.ModelAdmin):
    list_display = ['waktu', 'skor', 'produk']
    field = ['produk']
admin.site.register(ScoreMAE, tableSCORE)

class tableUserAct(admin.ModelAdmin):
    list_display = ['user', 'last_login']
    field = ['user']
admin.site.register(UserActivity, tableUserAct)
