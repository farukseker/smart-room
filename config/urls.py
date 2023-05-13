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
from django.urls import path

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from esp.models import Key


from django.urls import path


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




def mindex(request):
    return render(request,'esp_manage.html')

from esp.views import EspPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', EspPage.as_view(),name="esp_main"),
    path('api/trunon/',test_google)

]
