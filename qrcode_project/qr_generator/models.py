from django.db import models
import qrcode
from io import BytesIO
import base64

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

    @staticmethod
    def generate(data, user_id):
        image = qrcode.make(data)
        buffer = BytesIO()
        image.save(buffer, format='png')

        inf = base64.b64encode(buffer.getvalue())

        user = UserView.objects.get(id=user_id)

        qr = QRCodeView(qr_code=inf, owner=user)
        return qr

    @staticmethod
    def decode(user):
        result = []
        for data in user.qrcodeview_set.all():
            qr = data.qr_code
            info = f'data:image/png;base64,{qr.decode("UTF-8")}'
            result.append(info)
        return result
