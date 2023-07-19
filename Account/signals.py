import json
import redis
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from Account.models import CustomUserModel
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from Auth.models import OTPDevice
import qrcode
from io import BytesIO
import base64

import pyotp


@receiver(post_save, sender=CustomUserModel)
def send_message_to_socket(sender, instance, **kwargs):
    is_create_signal = kwargs.get("created")
    if is_create_signal:
        hash = pyotp.random_base32()
        OTPDevice.objects.create(
            hash_gen=hash,
            user=instance,
            is_active=True,
        )
        hash_gen = pyotp.TOTP(hash).provisioning_uri(name=instance.email, issuer_name=instance.username)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(hash_gen)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        buffered = BytesIO()
        img.save(buffered)
        encoded = base64.b64encode(buffered.getvalue()).decode()
        image = MIMEImage(buffered.getvalue())
        image.add_header('Content-ID', '<qrImage>')

        html_content = render_to_string('otp-mail.html',{
            'hash': hash,
            'encoded_hax': encoded
        })

        html_text = strip_tags(html_content)
        msg = EmailMultiAlternatives('OTP', html_text,
                               'settings.EMAIL_HOST_USER', (instance.email,))
        msg.attach(image)

        msg.attach_alternative(html_content, "text/html")
        msg.send()

