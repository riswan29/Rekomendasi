from django.db import models
from django.contrib.auth.models import AbstractUser


class customUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='img_profile')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Produk(models.Model):
    nama_barang = models.CharField(max_length=100)
    rating = models.FloatField()
    kategori = models.CharField(max_length=50)
    deskripsi = models.TextField()
    gambar1 = models.ImageField(upload_to='product_images/')
    gambar2 = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name