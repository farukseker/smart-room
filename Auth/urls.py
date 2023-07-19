from django.urls import path
from Auth.views import *

app_name = "Auth"
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('get-otp/', GetOtp.as_view(), name='get-otp'),
]
