from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('', anonim, name='usr'),
    path('formP/', formP, name='formP'),
    path('login', custom_login, name='login'),
    path('registrasi/', register, name='register'),
    path('prof/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('user/', user_dash, name='usr'),
    path('admin_dash/', admin_dash, name='adm'),
    # path('add/', add_product, name='add_produk'),
    path('list/', produk_list, name='list'),
    path('shop/', shop, name='shop'),
    path('produk/<int:produk_id>/', produk_detail, name='produk_detail'),
    path('recommendation/', recommendation_view, name='recommendation'),
    # path('excel/', tambah_produk_dari_excel, name='excel'),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
