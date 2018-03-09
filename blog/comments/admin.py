from django.contrib import admin
from comments.models import Comment
# Register your models here.
# admin background manage
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'article']
admin.site.register(Comment, CommentAdmin)
