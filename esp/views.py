from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView


class EspPage(TemplateView):
    template_name = "manage_esp_list.html"

    def get(self,request,*args,**kwargs):
        return super().get(request)

