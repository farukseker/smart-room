from django.shortcuts import render, redirect ,get_object_or_404, get_list_or_404, Http404
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.decorators import login_required
from esp.models import ESP, Key


class EspPage(View):
    def get(self, request, *args, **kwargs):
        # esp_list = ESP.objects.filter(user=request.user)
        esp_list: list = []

        for esp in ESP.objects.filter(user=request.user).order_by('name'):
            esp_list.append(esp)

        if esp_list:
            return render(request, template_name="manage_esp_list.html", context={
                "esp_list": esp_list
            })
        else:
            raise Http404('esp not found, u must be logged')

    def post(self, request):
        query_key_id = request.POST.get("key_id", None)
        key = get_object_or_404(Key, id=query_key_id)
        if key:
            esp_list = ESP.objects.filter(user=request.user)
            if key.owner_esp in esp_list:
                key.current = not key.current
                key.save()
        return redirect("esp_main")

    @classmethod
    def as_view(cls):
        return login_required(super(EspPage, cls).as_view())



from esp.models import Sensor

def test_eensor(request):
    sm = Sensor.objects.first()
    print(sm)
    sm.get_action()
    raise Http404("pars")