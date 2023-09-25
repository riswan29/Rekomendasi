from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', custom_login, name='login'),
    path('registrasi/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('user/', user_dash, name='usr'),
    path('admin_dash/', admin_dash, name='adm'),
    path('add/', add_product, name='add_produk'),
    path('list/', produk_list, name='list'),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

