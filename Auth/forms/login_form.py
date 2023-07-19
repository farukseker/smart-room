from django import forms


class user_login_form(forms.Form):
    name_or_email = forms.CharField(max_length=50,help_text='adınız')
    password = forms.CharField(widget=forms.PasswordInput)