from django import forms
from blog_app.models import Program


class MySpecialForm(forms.ModelForm):
    programs = forms.CharField()

    class Meta:
        model = Program
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)