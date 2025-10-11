from django.shortcuts import render, redirect ,get_object_or_404, get_list_or_404, Http404
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.decorators import login_required
from esp.models import ESP, Key


class EspPage(View):
    def get(self, request, *args, **kwargs):
        # Optimized query with prefetch_related to avoid N+1 queries
        esp_list = ESP.objects.filter(user=request.user).prefetch_related('keys').order_by('name')

        if esp_list.exists():
            return render(request, template_name="view_with_socket.html", context={
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
                key.set_current(not key.current, False)
                # key.current = not key.current
                # key.save()
        return redirect("esp_main")

    @classmethod
    def as_view(cls):
        return login_required(super(EspPage, cls).as_view())



from esp.models import SensorModel

def test_eensor(request):
    from django.utils import timezone

    raise Http404(",".join([str(timezone.now()),str(timezone.get_default_timezone()), str(timezone.tzinfo)]))