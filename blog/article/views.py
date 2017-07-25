#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
import markdown2
from article.models import Article,Category
# Create your views here.

class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            #将文本内容转换成markdown形式
            article.body = markdown2(article.body,)
        return article_list

    def get_context_data(self,**kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(IndexView,self).get_context_data(**kwargs)

def index(request):
    return render(request,"index.html",context={'title':'我的博客首页','welcome':'欢迎访问我的博客首页'})
