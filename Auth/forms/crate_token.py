from django import forms
from Auth.models import AuthToken


class TokenForum(forms.ModelForm):
    # life = forms.DateTimeField(required=False)
    class Meta:
        model = AuthToken
        fields = ('user',)
        exclude = ('life',)
