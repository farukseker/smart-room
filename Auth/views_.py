from django.shortcuts import render
from django.shortcuts import Http404
from django.shortcuts import redirect

from django.views.generic import View

from Auth.forms import user_login_form

from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib import messages

import datetime
from django.utils import timezone
from Auth.models import AuthToken


from Auth.forms import TokenForum


#
#
# class createLoginToken(View):
#
#     def get(self,request):
#         if request.user.is_authenticated and request.user.is_superuser:
#             form = TokenForum()
#             return render(request,template_name='select_user.html',context={'form':form})
#         else:
#             raise Http404
#     def post(self,request):
#         form = TokenForum(request.POST or None)
#         if request.user.is_authenticated and request.user.is_superuser and form.is_valid():
#             form.save(commit=False)
#             token_gen = AuthToken.objects.create(
#                 user=form.cleaned_data.get('user'),
#                 life=timezone.now() + datetime.timedelta(days=5)
#             )
#             return render(request,template_name='select_user.html',context={'form':form,'token':token_gen})
#         else:
#             return Http404
