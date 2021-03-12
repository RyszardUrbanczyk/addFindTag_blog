from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView
from blog_app.forms import LoginForm, RegisterForm,AddTagForm
from blog_app.models import Program, Tag
from django.views.generic.list import ListView
from django.urls import reverse


# Create your views here.


class BaseView(View):

    def get(self, request):
        return render(request, 'index.html')


class ProgramsListView(View):

    def get(self, request):
        ctx = {'objects': Program.objects.all().order_by('name')}
        return render(request, 'programs-list.html', ctx)


class AddProgramView(CreateView):
    template_name = 'add-program.html'
    model = Program
    fields = '__all__'
    success_url = '/programs-list/'


class EditProgramView(UpdateView):
    template_name = 'edit-program.html'
    model = Program
    fields = '__all__'
    success_url = '/programs-list/'


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                redirect_url = request.GET.get('next', 'index')
                # próbujemy pobrać ze słownika request.GET wartość która znajduje sie pod kluczem "next" jesli nie ma 'next'
                # to zwracamy "index"
                return redirect(redirect_url)
            else:
                return redirect('login')


class LogOutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            u = User.objects.create(username=username)
            u.set_password(password)
            u.save()
            return redirect('login')
        else:
            return render(request, 'form.html', {'form': form})


class AddTagView(CreateView):
    template_name = 'add-tag.html'
    model = Tag
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        ctx = {'form': AddTagForm()}
        return ctx

class TagsListView(View):

    def get(self, request):
        ctx = {'objects': Tag.objects.all()}
        return render(request, 'tags-list.html', ctx)

