from django.contrib import admin
from blog_app.models import Tag, Program, Post, Comment, Gallery, Image

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "body",)

admin.site.register(Tag)
admin.site.register(Program)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Gallery)
admin.site.register(Image)
