from django.views import View
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView

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
