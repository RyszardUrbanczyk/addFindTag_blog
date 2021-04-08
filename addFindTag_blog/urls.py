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
from django.urls import path, include
from blog_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.BaseView.as_view(), name='index'),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('accounts/profile/', views.BaseView.as_view(), name='index'),

                  # path('login/', views.LoginView.as_view(), name='login'),
                  # path('logout/', views.LogOutView.as_view(), name='logout'),
                  path('register/', views.RegisterView.as_view(), name='register'),
                  path('program-list/', views.ProgramListView.as_view(), name='program-list'),
                  path('program-detail/<int:pk>/', views.ProgramDetailView.as_view(), name='program-detail'),
                  path('add-program/', views.AddProgramView.as_view(), name='add-program'),
                  # path('post-list/', views.PostListView.as_view(), name='post-list'),
                  path('add-post/', views.AddPostView.as_view(), name='add-post'),
                  path('edit-post/<int:id>/', views.EditPostView.as_view(), name='edit-post'),
                  path('add-comment/<int:id>/', views.AddCommentView.as_view(), name='add-comment'),
                  path('add-tag/', views.AddTag.as_view(), name='add-tag'),
                  path('post-user/', views.ListPostLoggedUser.as_view(), name='post-user'),
                  path('add-gallery/', views.AddGalleryView.as_view(), name='add-gallery'),
                  path('gallery-list/', views.GalleryListView.as_view(), name='gallery-list'),
                  path('add-image/', views.AddImageToGalleryView.as_view(), name='add-image'),
                  path('gallery-detail/<int:id>/', views.GalleryDetailView.as_view(), name='gallery-detail'),
                  path('search/', views.FindPostView.as_view(), name='search'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
