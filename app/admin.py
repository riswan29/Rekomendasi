from django.contrib import admin
from .models import *


class tableUser(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'is_staff', 'is_active','image',]
    fields = ['image']
admin.site.register(customUser, tableUser)

admin.site.register(Produk)

