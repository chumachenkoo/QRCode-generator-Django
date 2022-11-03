from django.db import models

# Create your models here.


class UserView(models.Model):
    username = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=25, null=False)

    objects = models.Manager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class QRCodeView(models.Model):
    qr_code = models.BinaryField(null=False)
    owner = models.ForeignKey(UserView, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = 'QRCode'
        verbose_name_plural = 'QRCodes'
