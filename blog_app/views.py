from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView
from blog_app.forms import AddPostForm, LoginForm, RegisterForm

from blog_app.models import Tag, Post


# Create your views here.


class BaseView(View):
    """
    Base view: when the user enters the first page.
    """

    def get(self, request):
        return render(request, 'index.html')


class TagListView(View):
    """
    View of list tags-programs.
    """

    def get(self, request):
        ctx = {'objects': Tag.objects.all().order_by('name')}
        return render(request, 'tag-list.html', ctx)


class AddTagView(CreateView):
    """
    In this View is form to adding tags to database.
    """
    template_name = 'add-program.html'
    model = Tag
    fields = '__all__'
    success_url = '/tag-list/'


class PostListView(View):

    def get(self, request):
        posts = Post.objects.all()
        # tags = [{'title': t.title, 'body': t.body, 'programs': t.programs.values_list('name', flat=True)} for t in tags]
        ctx = {'objects': posts}

        return render(request, 'post-list.html', ctx)


class AddPostView(CreateView):
    template_name = 'add-post.html'
    model = Post
    fields = '__all__'
    success_url = '/post-list/'

    def get_context_data(self, **kwargs):
        ctx = {'form': AddPostForm()}
        return ctx


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