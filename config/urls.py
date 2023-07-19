"""smart_room URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse,JsonResponse

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from esp.models import Key


from django.urls import path, include

from Auth import views as auth_view


@csrf_exempt
@xframe_options_exempt
def test_google(request):

    if request.method == "POST":
        try:
            key = Key.objects.get(pin_name="LAMBA_PIN")
            key.current = not key.current
            key.save()
        except Exception as e:
            print(e)
            pass
        return JsonResponse({"status":200})
    else:
        return JsonResponse({"status":200,"markus":"parse"})


from django.contrib.auth import get_user_model

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import qrcode
from io import BytesIO
import base64

import pyotp


user_model = get_user_model()

def mindex(request):

    return render(request, 'esp_manage.html')

from esp.views import EspPage, test_eensor

urlpatterns = [
    path('admin/login/', auth_view.CustomAdminLogin.as_view(), name='login'),
    path('admin/get-otp/', auth_view.GetOtp.as_view(), name='get-otp'),
    path('admin/otp/', auth_view.OTPView.as_view(), name='otp-admin'),
    path('admin/', admin.site.urls),
    path('', EspPage.as_view(), name="esp_main"),
    path('sensor/', test_eensor),
    path('mail/', mindex),
    path('api/', include('api.urls')),
]
