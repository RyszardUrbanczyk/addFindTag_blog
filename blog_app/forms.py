from django import forms
from django.core.exceptions import ValidationError

from blog_app.models import Program, Post, Tag, Comment


class AddPostForm(forms.ModelForm):
    programs = forms.ModelMultipleChoiceField(queryset=Program.objects.order_by('name'),
                                              widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "off"}))
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise ValidationError("Hasła się nie zgadzają")


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['post']