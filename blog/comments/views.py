#-*- coding:utf-8 -*-
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from article.models import Article
from .models import Comment
from .forms import CommentForm

def article_comment(request,article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    
    if request.method == 'POST':
        #构造CommentForm实例，生成django表单
        form = CommentForm(request.POST)
        #判断合法性
        if form.is_valid():
            #检查数据的合法性，调用表单的save将评论保存到数据库中
            #commit=False仅仅是生成了模型类的实例，但是还并没有保存到数据库中
            comment = form.save(commit=False)
            comment.article = article
            #保存评论
            comment.save()
            return HttpResponseRedirect('/index/'+article_pk+'/')

        else:
            #检测数据不合法，反向获取所有评论渲染给模板
            #通过Article.comment_set.all()获取
            #Article和Comment是通过foreignkey进行关联的
            comment_list = article.comment_set.all()
            context = {'article':article,
                       'form':form,
                       'comment_list':comment_list
                      }
            return render(request,'detail.html',context=context)

    #不是POST返回文章详情页，还需要修改路由！！！！
    return HttpResponseRedirect('/index'+article_pk+'/')
