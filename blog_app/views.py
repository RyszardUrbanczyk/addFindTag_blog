from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from blog_app.forms import AddPostForm, RegisterForm, AddCommentForm, AddTagForm, \
    AddImageForm, EditPostForm, SearchForm
from blog_app.models import Program, Post, Tag, Comment, Gallery


# Create your views here.


class BaseView(View):
    """
    Base view: when the user enters the first page.
    """

    def get(self, request):
        return render(request, 'base.html')


class ProgramListView(ListView):
    """
    List of all programs that are topics
    for information exchange on the site.
    """
    queryset = Program.objects.all().order_by('date_added')
    context_object_name = 'objects'
    # paginate_by = 2
    template_name = 'program-list.html'


class ProgramDetailView(LoginRequiredMixin, View):
    """
    View of a specific blog program / topic.
    """

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
               'tags': tags,
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


class AddPostView(LoginRequiredMixin, CreateView):
    """
    In this View is form to adding posts to database.
    """
    template_name = 'add-post.html'
    form_class = AddPostForm
    success_url = '/program-list/'

    def form_valid(self, form):
        """
        We automatically pass the author field to the form,
        which is the name of the logged in user.
        """
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(self.success_url)


class RegisterView(View):
    """
    New user registration view.
    """

    def get(self, request):
        form = RegisterForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # if User.objects.filter(username=username).exists():
            #     m = f'Isnieje taki użytkownik.'
            #     return render(request, 'form.html', {'form': form, 'm':m})
            u = User.objects.create(username=username)
            u.set_password(password)
            u.save()
            return redirect('login')
        else:
            return render(request, 'form.html', {'form': form})


class AddCommentView(LoginRequiredMixin, View):
    """
    This view provides a form for adding comments to the database.
    Comments about a specific(id) entry on the site.
    """

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
    """
    User can add tags to selected programs.
    """
    template_name = 'add-tag.html'
    model = Tag
    fields = '__all__'
    success_url = '/program-list/'

    def get_context_data(self, **kwargs):
        ctx = {'form': AddTagForm()}
        return ctx


class ListPostLoggedUser(View):
    """
    The user can view the list of all his entries.
    """

    def get(self, request):
        posts = Post.objects.filter(author=request.user)
        return render(request, 'list-logged-user.html', {'posts': posts})


class AddGalleryView(LoginRequiredMixin, CreateView):
    """
    In this view, the user can add a new gallery and its description.
    """
    template_name = 'add-gallery.html'
    model = Gallery
    fields = '__all__'
    success_url = '/gallery-list/'


class GalleryListView(ListView):
    """
    List of all galleries.
    """
    queryset = Gallery.objects.all()
    context_object_name = 'objects'
    template_name = 'gallery-list.html'


class AddImageToGalleryView(LoginRequiredMixin, CreateView):
    """
    The user can add a picture to the selected gallery.
    """
    template_name = 'add-image-to-gallery.html'
    form_class = AddImageForm
    success_url = '/add-image/?success=true'

    def form_valid(self, form):
        """
        We automatically pass the author field to the form,
        which is the name of the logged in user.
        """
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
    """
    Specific gallery view.
    """

    def get(self, request, id):
        object = Gallery.objects.get(id=id)
        images = object.image_set.all()
        return render(request, 'gallery-detail.html', {'images': images})


class EditPostView(View):
    """
    View of edit post.
    """

    def get(self, request, id):
        post = Post.objects.get(id=id)
        if post.author != request.user:
            raise Http404
        else:  # Only the owner of the post can edit his post.
            form = EditPostForm(instance=post)
            return render(request, 'edit-post.html', {'form': form})

    def post(self, request, id):
        post = Post.objects.get(id=id)
        form = EditPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('program-list')
        return render(request, 'edit-post.html', {'form': form})


class FindPostTagView(View):
    """
    Search post and tags
    """

    def get(self, request):
        search = request.GET.get('query')
        if search == '':
            m = f'Wpisz szukane słowo.'
            return render(request, 'find.html', {'m': m})

        if search is not None:
            object_list = Post.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
            tags = Tag.objects.filter(name__icontains=search)
            programs = Program.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
            sum_of_search = len(object_list) + len(tags) + len(programs)
            if sum_of_search == 0:
                mk = f'Nic nie znaleziono.'
                return render(request, 'find.html', {'mk': mk})
            return render(request, 'find.html', {'object_list': object_list,
                                                 'tags': tags,
                                                 'programs': programs,
                                                 'sum_of_search': sum_of_search})

        return render(request, 'find.html')

# class FindPostTagView(ListView):
#     model = Post
#     template_name = 'find.html'
#
#     def get_queryset(self):
#         search = self.request.GET.get('query')
#         if search == '':
#             m = f'Wpisz szukane słowo'
#             return m
#         if search is not None:
#
#             object_list = Post.objects.filter(
#                 Q(title__icontains=search) | Q(body__icontains=search)
#             )
#             return object_list
