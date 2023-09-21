from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_dash.urls')),
    path('', include('app.urls')),
]
