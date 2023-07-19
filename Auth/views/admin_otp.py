from django.views.generic import View
from django.shortcuts import redirect
from django.shortcuts import render
from Auth.models import OTPDevice
from django.contrib.auth import login, authenticate

import pyotp


class OTPView(View):
    template_name = "admin/otp.html"

    def get(self, request):
        session_authorization = self.request.session.get('session_authorization')
        if session_authorization and request.user.is_authenticated:
            return redirect('admin:index')
        elif request.user.is_authenticated and not session_authorization:
            return render(request, template_name="admin/otp.html")
        else:
            return redirect('login')

    def post(self,request):
        session_authorization = self.request.session.get('session_authorization')
        user = request.user
        otp_code = request.POST.get('otp', None)

        if user.is_authenticated and not session_authorization and otp_code:
            otp_models = OTPDevice.objects.filter(user_id=user.id)
            for otp_model in otp_models:
                if otp_model.is_active:
                    totp = pyotp.TOTP(otp_model.hash_gen)
                    if totp.verify(otp_code):  # => True
                        self.request.session.__setitem__('session_authorization', True)
                        return redirect('admin:index')

            return render(request,template_name="admin/otp.html")
        else:
            return render(request, template_name="admin/otp.html")
