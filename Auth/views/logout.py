from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth import logout


class Logout(View):
    def post(self,request):
        response = redirect('Auth:login')
        logout(request)
        return response