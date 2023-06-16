from django.contrib import admin
from . import models
# Register your models here.

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, reverse, resolve
from django import forms

admin.site.register(models.ESP)
# admin.site.register(models.Key)
admin.site.register(models.TimeRanger)


class KeyModelAdminForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'range-time-input'}), required=False)
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'range-time-input'}), required=False)

    class Meta:
        model = models.Key
        fields = '__all__'


class KeyModelAdmin(admin.ModelAdmin):
    form = KeyModelAdminForm

    class Media:
        js = ('js/key_time_range.js',)
        # css = {
        #     'all': ('css/admin/my_own_admin.css',)
        # }


admin.site.register(models.Key, KeyModelAdmin)