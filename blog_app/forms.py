from django import forms
from django.core.exceptions import ValidationError

from blog_app.models import Program


class MySpecialForm(forms.ModelForm):
    programs = forms.CharField()

    class Meta:
        model = Program
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class RegisterForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete":"off"}))
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise ValidationError("Hasła się nie zgadzają")