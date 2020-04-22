from django.db import models


# Create your models here.
class UserPhone(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='userphone', on_delete=models.CASCADE)
    no_HP = models.CharField(max_length=12)


class UserID(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    no_HP = models.ForeignKey(UserPhone, related_name='userid', on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    nik = models.CharField(max_length=16)
    alamat = models.TextField()
    tanggal_lahir = models.CharField(max_length=8)

    class Meta:
        ordering = ['nama']


class Form(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    gejala_demam = models.BooleanField(default=False)
    usia = models.BooleanField(default=False)
    kontak = models.BooleanField(default=False)
    aktivitas = models.BooleanField(default=False)
    gejala_lain = models.TextField()
    kategori = models.PositiveSmallIntegerField(default=0)
    userid = models.ForeignKey(UserID, related_name='forms', on_delete=models.CASCADE)

