from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView
from blog_app.forms import MySpecialForm
from blog_app.models import Program
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
    # form_class = MySpecialForm

#
#
# class EditProductView(UpdateView):
#     template_name = 'edit-product.html'
#     model = Product
#     # fields = '__all__'
#     success_url = '/products/'
#     form_class = MySpecialForm