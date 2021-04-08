from django import forms
from django.core.exceptions import ValidationError

from blog_app.models import Program, Post, Tag, Comment, Gallery, Image


class AddPostForm(forms.ModelForm):
    programs = forms.ModelChoiceField(queryset=Program.objects.order_by('name'),
                                      widget=forms.RadioSelect)

    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['author']


class AddImageForm(forms.ModelForm):
    galleries = forms.ModelChoiceField(queryset=Gallery.objects.order_by('name'),
                                       widget=forms.RadioSelect)

    class Meta:
        model = Image
        # fields = '__all__'
        exclude = ['author']


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


class AddTagForm(forms.ModelForm):
    applications = forms.ModelMultipleChoiceField(queryset=Program.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Tag
        fields = '__all__'


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'body_image', 'programs']
        fields = '__all__'


class SearchForm(forms.Form):
    szukaj = forms.CharField()
