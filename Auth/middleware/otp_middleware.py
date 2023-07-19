from django.shortcuts import reverse
from django.shortcuts import redirect


class OTPMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = reverse('admin:index')
        response = self.get_response(request)
        otp_gen = request.session.get('session_authorization', None)  # False None | True
        if request.path.startswith(path):
            if request.path == reverse("admin:login") or request.path == reverse("otp-admin") or request.path == reverse("get-otp") or otp_gen:
                pass
            else:
                response = redirect(reverse("admin:login"))
        return response


