from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from blog_app.forms import AddPostForm, RegisterForm, AddCommentForm, AddTagForm, AddImageForm

from blog_app.models import Program, Post, Tag, Comment, Gallery, Image


# Create your views here.


class BaseView(View):
    """
    Base view: when the user enters the first page.
    """

    def get(self, request):
        return render(request, 'base.html')


class ProgramListView(ListView):
    queryset = Program.objects.all()
    context_object_name = 'objects'
    # paginate_by = 2
    template_name = 'program-list.html'


# class ProgramDetailView(LoginRequiredMixin, View):
#
#     def get(self, request, pk):
#         program = Program.objects.get(pk=pk)
#         posts = program.post_set.all()
#         tags = program.tag_set.all()
#         ctx = {'program': program,
#                'posts': posts,
#                'tags': tags
#                }
#
#         return render(request, 'program-detail.html', ctx)


class ProgramDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        program = Program.objects.get(pk=pk)
        posts = program.post_set.all().order_by('-publish')
        tags = program.tag_set.all()
        paginator = Paginator(posts, 3)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        ctx = {'program': program,
               'posts': posts,
               'tags': tags
               }

        return render(request, 'program-detail.html', ctx)


# class PostListView(LoginRequiredMixin, View):
#
#     def get(self, request):
#         objects = Post.objects.all()
#         paginator = Paginator(objects, 2)
#         page = request.GET.get('page')
#         try:
#             objects = paginator.page(page)
#         except PageNotAnInteger:
#             objects = paginator.page(1)
#         except EmptyPage:
#             objects = paginator.page(paginator.num_pages)
#
#         ctx = {
#                'page':page,
#                'objects':objects
#                }
#
#         return render(request, 'post-list.html', ctx)


class AddProgramView(LoginRequiredMixin, CreateView):
    """
    In this View is form to adding programs to database.
    """
    template_name = 'add-program.html'
    model = Program
    fields = '__all__'
    success_url = '/program-list/'


# class PostListView(View):
#
#     def get(self, request):
#         posts = Post.objects.all()
#         # posts = [{'title': p.title, 'body': p.body, 'programs': p.programs.values_list('name', flat=True)} for p in po]
#         ctx = {'objects': posts}
#         return render(request, 'post-list.html', ctx)


class AddPostView(LoginRequiredMixin, CreateView):
    template_name = 'add-post.html'
    form_class = AddPostForm
    success_url = '/program-list/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(self.success_url)


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


# 1 wersja działa
# class AddCommentView(View):
#
#     def get(self, request, id):
#         post = Post.objects.get(id=id)
#         # comments = post.comment_set.all()
#         return render(request, 'add-comment.html', {'post': post})
#
#     def post(self, request, id):
#         post_id = Post.objects.get(id=id)
#         name = request.POST['name']
#         body = request.POST['body']
#         comment = Comment.objects.create(name=name, body=body, post=post_id)
#         return redirect(reverse('program-list'))

# 2 wersja działa
class AddCommentView(LoginRequiredMixin, View):

    def get(self, request, id):
        form = AddCommentForm()
        return render(request, 'add-comment.html', {'form': form})

    def post(self, request, id):
        form = AddCommentForm(request.POST)
        post_id = Post.objects.get(id=id)
        if form.is_valid():
            Comment.objects.create(**form.cleaned_data, post=post_id)
            return redirect('program-list')
        return render(request, 'add-comment.html', {'form': form})


class AddTag(LoginRequiredMixin, CreateView):
    template_name = 'add-tag.html'
    model = Tag
    fields = '__all__'
    success_url = '/program-list/'

    def get_context_data(self, **kwargs):
        ctx = {'form': AddTagForm()}
        return ctx


class ListPostLoggedUser(View):

    def get(self, request):
        posts = Post.objects.filter(author=request.user)
        return render(request, 'list-logged-user.html', {'posts': posts})


class AddGalleryView(LoginRequiredMixin, CreateView):
    template_name = 'add-gallery.html'
    model = Gallery
    fields = '__all__'
    success_url = '/gallery-list/'


class GalleryListView(ListView):
    queryset = Gallery.objects.all()
    context_object_name = 'objects'
    # paginate_by = 2
    template_name = 'gallery-list.html'


class AddImageToGalleryView(LoginRequiredMixin, CreateView):
    template_name = 'add-image-to-gallery.html'
    form_class = AddImageForm
    success_url = '/add-image/'


    def form_valid(self, form):
        image = form.save(commit=False)
        image.author = self.request.user
        image.save()
        return redirect(self.success_url)

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data()
    #     message = f'Dodaj kolejny'
    #     if self.success_url:
    #         ctx.update({'message': message})
    #         return ctx



class GalleryDetailView(LoginRequiredMixin, View):

    def get(self, request, id):
        object = Gallery.objects.get(id=id)
        images = object.image_set.all()
        return render(request, 'gallery-detail.html', {'images':images})