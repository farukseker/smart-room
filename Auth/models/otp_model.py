from django.db import models


class OTPDevice(models.Model):
    user = models.ForeignKey('Account.CustomUserModel',on_delete=models.CASCADE,default=None,blank=True)
    hash_gen = models.TextField(max_length=50,editable=True)
    is_active = models.BooleanField(default=True)

    def create_hash(self):
        import pyotp
        return pyotp.TOTP(self.hash_gen).provisioning_uri(name=self.user.email,issuer_name=self.user.username)


    def qr_code(self):
        import pyotp

    def load_otp(self):
        pass

    def otp_verify(self):
        pass