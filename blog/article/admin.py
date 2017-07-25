from django.contrib import admin
from article.models import Article,Category
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','last_modified_time','status','views','likes']
    search_fields = ['title']
    list_fields = ['status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','created_time','last_modified_time']
    search_fields = ['name']
    list_fields = ['created_time']

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)
