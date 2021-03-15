from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView
from blog_app.forms import AddPostForm, LoginForm, RegisterForm

from blog_app.models import Program, Post, Tag, Comment


# Create your views here.


class BaseView(View):
    """
    Base view: when the user enters the first page.
    """

    def get(self, request):
        return render(request, 'index.html')


class ProgramListView(View):
    """
    View of list programs.
    """

    def get(self, request):
        ctx = {'objects': Program.objects.all().order_by('name')}
        return render(request, 'program-list.html', ctx)


class ProgramDetailView(View):

    def get(self, request, pk):
        program = Program.objects.get(pk=pk)
        posts = program.post_set.all()
        # post = program.post_set.all().first()
        # comments = post.comment_set.all()
        # tags = program.tag_set.all()
        ctx = {'program': program,
               'posts': posts,
               }

        return render(request, 'program-detail.html', ctx)


class AddProgramView(LoginRequiredMixin, CreateView):
    """
    In this View is form to adding programs to database.
    """
    template_name = 'add-program.html'
    model = Program
    fields = '__all__'
    success_url = '/program-list/'


class PostListView(View):

    def get(self, request):
        posts = Post.objects.all()
        # posts = [{'title': p.title, 'body': p.body, 'programs': p.programs.values_list('name', flat=True)} for p in po]
        ctx = {'objects': posts}
        return render(request, 'post-list.html', ctx)


class AddPostView(LoginRequiredMixin, CreateView):
    template_name = 'add-post.html'
    model = Post
    fields = '__all__'
    success_url = '/program-list/'

    def get_context_data(self, **kwargs):
        ctx = {'form': AddPostForm()}
        return ctx


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


class AddCommentView(View):

    def get(self, request, id):
        post = Post.objects.get(id=id)
        comments = post.comment_set.all()
        return render(request, 'add-comment.html', {'post': post, 'comments':comments})

    def post(self, request, id):
        post_id = Post.objects.get(id=id)
        name = request.POST['name']
        body = request.POST['body']
        comment = Comment.objects.create(name=name, body=body, post=post_id)
        return redirect(reverse('program-list'))