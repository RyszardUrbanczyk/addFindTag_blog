"""addFindTag_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.BaseView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('tag-list/', views.TagListView.as_view(), name='tag-list'),
    path('tag-detail/<int:id>', views.TagDetailView.as_view(), name='tag-detail'),
    path('add-tag/', views.AddTagView.as_view(), name='add-tag'),
    path('post-list/', views.PostListView.as_view(), name='post-list'),
    path('add-post/', views.AddPostView.as_view(), name='add-post'),
]
