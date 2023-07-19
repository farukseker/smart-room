from django.contrib import admin
from Auth.models import AuthToken
from django.urls import path,include

from Auth.models import OTPDevice
admin.site.register(AuthToken)
# admin.site.register(OTPDevice)

# Register your models here.
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.html import format_html


@admin.register(OTPDevice)
class OTPDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active')
    readonly_fields = ['qrcode']

    def qrcode(self, obj):
        try:
            import qrcode
            from io import BytesIO
            import base64

            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(obj.create_hash())
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            encoded = base64.b64encode(buffered.getvalue()).decode()

            return format_html(f'<img width="200px" height="200px" src="data:image/png;base64,{encoded}">')

        except Exception as e:
            raise e
    qrcode.short_description = "QR Code"



    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super().get_fieldsets(request,obj)
    #     fieldsets.append(
    #         (None, {
    #             'fields': ['qrcode'],
    #         }),
    #     )
    #     return fieldsets


# admin.site.register(OTPDevice,OTPDeviceAdmin)