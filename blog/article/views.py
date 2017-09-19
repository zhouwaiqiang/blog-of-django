#-*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.list import ListView
import markdown2
import markdown
from comments.forms import CommentForm
from article.models import Article,Category,Tag
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

class IndexView(ListView):
    #没有queryset方法直接指定数据库名即可
    #model = Article
    template_name = "index.html"
    #模型数据传递给模板的名字
    context_object_name = "article_list"
    paginate_by = 3

    #重写ListView类中的get_queryset方法,该方法是为了获取Model的列表
    def get_queryset(self):
        article_list = Article.objects.all()
        for article in article_list:
            article.body = markdown.markdown(article.body,extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc',])
        return article_list

    def get_context_data(self,**kwargs):
        #在类视图中，传递模板变量字典通过get_context_data函数获得，现在复写该方法
        #使得插入一些我们自定义的模板变量进去

        #首先获得父类生成的传递给模板的字典
        context = super(IndexView,self).get_context_data(**kwargs)

        #父类生成的字典中已有paginator、page_obj、is_paginated这三个模板变量
        #paginator是Paginator的一个实例
        #page_obj是Page的一个实例
        #is_paginated是一个布尔变量，用于指示是否已分页
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        #调用自己写的pagination_data方法获得显示分页导航条需要的数据
        pagination_data = self.pagination_data(paginator,page,is_paginated)

        #将分页导航条的模板更新到context中
        context.update(pagination_data)
        #将需要渲染模板的数据返回，此时context已有分页导航条的所有数据
        return context

    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            #如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据
            #因此返回一个空的字典
            return {}
        #当前页左连续的页码号，初始值为空
        left = []

        #当前页右连续的页码号，初始值为空
        right = []

        #标示第一页页码后是否需要显示省略号
        left_has_more = False

        #表示最后一页页码前是否需要显示省略号
        right_has_more = False

        #标示是否需要显示第一页的页码号
        #因为如果当前页左边的连续页码号中已经含有第一页的页码号，此时就无需再显示第一页的页码号
        #其他情况下第一页的页码是始终需要显示的
        first = False

        #标示是否需要显示最后一页的页码号
        last = False

        #获得用户当前请求的页码号
        page_number = page.number

        #获得分页后的总页数
        total_pages = paginator.num_pages

        #python3中获得分页页码列表，比如分了四页，则是[1,2,3,4]的列表
        #python2中返回的xrange对象，并且列表，不能做slice操作,需要list转成列表
        page_range = list(paginator.page_range)

        #range操作是从0开始，页码从1开始，所以在后台代码中要把页码的数量-1进行操作
        if page_number == 1:
            #如果用户当前请求的是第一页的数据，那么当前页左边的不需要数据，因此left=[]
            #获取当前页右边的连续页码号
            #比如分页页码表是[1,2,3,4],那么获得便是right=[2,3]
            #这里只获得了当前页码后连续两个页码，可以更改这个数字获得更多的页码
            #python中利用range函数，并且使用try对右边界进行边界控制
            right = page_range[page_number:page_number + 1]

            #如果最右边的页码号比最后一页的页码减去1还小
            #说明最右边的页码号和最后一页的页码间还有其他页码，因此需要显示省略号
            if right[-1] < total_pages - 1:
                right_has_more = True

            #如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码中不会显示最后一页页码
            #所以需要显示最后一页的页码，通过last表示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            #如果当前用户获取的是最后一页的页码，那么就不需要右边的数据
            #只需要请求左边的数据，和上面的内容类似
            left = page_range[(page_number -2) if (page_number - 2) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            #如果既不是第一页也不是最后一页，那么就需要结合上面的二者
            left = page_range[(page_number - 2) if (page_number - 2) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 1]

            #是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True


            #是否需要显示第一页和第一页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        context = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
                }
        return context


def index(request):
    #article_list = Article.objects.all().order_by('-created_time')
    article_list = Article.objects.all()
    #分页，每页10条数据
    paginator = Paginator(article_list,10)
    #获取当前页码
    page = request.GET.get('page')

    try:
        #获取当前页的内容
        article_list = paginator.page(page)
    except PageNotAnInteger:
        #获取第一页的内容
        article_list = paginator.page(1)
    except EmptyPage:
        #超出页码范围，默认使用最后一页
        article_list = paginator.page(paginator.num_pages)
    return render(request,"index.html",context={'article_list':article_list})

def archives(request,year,month):
    article_list = Article.objects.filter(created_time__year=year,created_time__month=month).order_by('-created_time')
    for article in article_list:
        article.body = markdown.markdown(article.body,extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',])
    return render(request,"index.html",context={'article_list':article_list})

def detail(request,pk):
    article = get_object_or_404(Article,pk=pk)
    #增加阅读量
    article.increase_views()
    article.body = markdown.markdown(article.body,extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    form = CommentForm()
    #获取下方所有评论
    comment_list = article.comment_set.all()
    context = {'article':article,
               'form':form,
               'comment_list':comment_list
              }
    return render(request,'detail.html',context=context)

def category(request,pk):
    category_name = get_object_or_404(Category,pk=pk)
    article_list = Article.objects.filter(category=category_name).order_by('-created_time')
    for article in article_list:
        article.body = markdown.markdown(article.body,extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',])
    return render(request,"index.html",context={'article_list':article_list})

def search(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        error_msg = ''
        if not question:
            error_msg = "请输入关键词"
            return render(request,'index.html',context={'error_msg':error_msg})
        article_list = Article.objects.filter(title__icontains=question)
        for article in article_list:
            article.body = markdown.markdown(article.body,extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc',])
        return render(request,'index.html',context={'error_msg':error_msg,'article_list':article_list})
    else:
        pass

#标签云路由处理
def tag(request,tag_id):
    tag_name = get_object_or_404(Tag,pk=tag_id)
    article_list = Article.objects.filter(tag=tag_name).order_by('-created_time')
    for article in article_list:
        article.body = markdown.markdown(article.body,extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',])
    return render(request,'index.html',context={'article_list':article_list})

def page_not_found(request):
    #这是处理400页面的函数
    return render(request,'404.html')
