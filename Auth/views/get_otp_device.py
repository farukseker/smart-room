import base64
from email.mime.image import MIMEImage
from io import BytesIO

import pyotp
import qrcode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from Auth.models import OTPDevice
from django.contrib.auth import get_user_model


user_model = get_user_model()

class GetOtp(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/get-otp.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('otp-email', None)
        hash_gen = None
        hash_token = None
        if otp_device := OTPDevice.objects.filter(user__email=email, is_active=True).first():
            hash_token = otp_device.hash_gen
            hash_gen = pyotp.TOTP(hash_token).provisioning_uri(name=otp_device.user.email, issuer_name=otp_device.user.username)

        else:
            if user := user_model.objects.filter(email=email).first():
                hash_token = pyotp.random_base32()
                OTPDevice.objects.create(
                    hash_gen=hash_token,
                    user=user,
                    is_active=True,
                )
                hash_gen = pyotp.TOTP(hash_token).provisioning_uri(name=user.email, issuer_name=user.username)

        if hash_gen is not None:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(hash_gen)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')
            buffered = BytesIO()
            img.save(buffered)
            encoded = base64.b64encode(buffered.getvalue()).decode()
            image = MIMEImage(buffered.getvalue())
            image.add_header('Content-ID', '<qrImage>')

            html_content = render_to_string('otp-mail.html', {
                'hash': hash_token,
                'encoded_hax': encoded
            })

            html_text = strip_tags(html_content)
            msg = EmailMultiAlternatives('OTP', html_text,
                                         'settings.EMAIL_HOST_USER', (email,))
            msg.attach(image)

            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return redirect(reverse('otp-admin'))
