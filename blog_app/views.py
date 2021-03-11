from django.shortcuts import render, redirect
from django.views import View
from blog_app.models import Program
from django.views.generic.list import ListView
from django.urls import reverse


# Create your views here.


class BaseView(View):

    def get(self, request):
        ctx = {'objects': Program.objects.all()}
        return render(request, 'base.html', ctx)


class ProgramsListView(View):

    def get(self, request):
        objects = Program.objects.all()
        ctx = {'objects': objects}
        return render(request, 'programs-list.html', ctx)


class ProgramModifyView(View):

    def get(self, request, id):
        ctx = {'object_id': Program.objects.get(id=id)}
        return render(request, 'program-modify.html', ctx)

    def post(self, request, id):
        pass

