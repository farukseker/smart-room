import pyotp
from django.db import models


class OTPDevice(models.Model):
    user = models.ForeignKey('Account.CustomUserModel',on_delete=models.CASCADE,default=None,blank=True)
    hash_gen = models.TextField(max_length=50,editable=True)
    is_active = models.BooleanField(default=True)

    def create_hash(self):
        return pyotp.TOTP(self.hash_gen).provisioning_uri(name=self.user.email, issuer_name=self.user.username)

    def qr_code(self):
        import pyotp

    def load_otp(self):
        pass

    @classmethod
    def otp_verify(cls, user, otp_code):
        if cls.user_has_otp_device(user):
            otp_devices = cls.objects.filter(user=user)
            for otp_device in otp_devices:
                if otp_device.is_active:
                    totp = pyotp.TOTP(otp_device.hash_gen)
                    if totp.verify(otp_code):
                        return True

    @classmethod
    def user_has_otp_device(cls, user):
        return cls.objects.filter(user=user).exists()