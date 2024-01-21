from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


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
    tipe_motor = models.CharField(max_length=100)
    jenis_ban = models.CharField(max_length=100, blank=False)
    rating = models.FloatField()
    ukuran = models.CharField(max_length=20)
    harga = models.IntegerField()
    deskripsi = models.TextField()
    gambar1 = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.nama_barang


class ScoreMAE(models.Model):
    waktu = models.DateTimeField(auto_now_add=True)
    skor = models.FloatField()
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.produk.nama_barang} - {self.waktu}"


class UserActivity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True)
    login_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Last Login: {self.last_login}"

    def update_activity(self):
        self.last_login = self.user.last_login
        self.login_count += 1
        self.save()

    @receiver(post_save, sender=get_user_model())
    def user_created(sender, instance, created, **kwargs):
        """
        Signal handler to update UserActivity when a new user is created.
        """
        if created:
            UserActivity.objects.create(user=instance)
