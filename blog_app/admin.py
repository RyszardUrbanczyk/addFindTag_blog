from django.contrib import admin
from blog_app.models import Tag, Program, Post, Comment
# Register your models here.

admin.site.register(Tag)
admin.site.register(Program)
admin.site.register(Post)
admin.site.register(Comment)