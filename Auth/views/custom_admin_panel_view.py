from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate


class CustomAdminLogin(LoginView):
    form_class = AuthenticationForm
    authentication_form = None
    template_name = "admin/customized-login-admin.html"
    redirect_authenticated_user = False
    extra_context = None

    def form_valid(self, form):

        """Security check complete. Log the user in."""
        login(self.request,form.get_user())
        # self.request.session.__setitem__('session_authorization',False)
        return redirect('otp-admin')
