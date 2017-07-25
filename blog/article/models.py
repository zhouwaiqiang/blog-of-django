#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Article(models.Model):
    STATUS_CHOICES =(('d','Draft'),('p','Published'),)
    title = models.CharField('标题',max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    last_modified_time = models.DateTimeField('最后修改时间',auto_now=True)
    status = models.CharField('文章状态',max_length=1,choices=STATUS_CHOICES)
    abstract = models.CharField('摘要',max_length=54,blank=True,null=True,help_text="可选，如若为空将摘取正文的前54个字符")
    views = models.PositiveIntegerField('浏览数',default=0)
    likes = models.PositiveIntegerField('点赞数',default=0)
    topped = models.BooleanField('置顶',default=False)
    category = models.ForeignKey('Category',verbose_name='分类',null=True,on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.title

    #如果是python3则应该如下
    #def __str__(self):
     #   return self.title

    class Meta:
        #django内部类定义Django模型的一些行为特性
        ordering = ['-last_modified_time']

class Category(models.Model):
    name = models.CharField('类名',max_length=20)
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    last_modified_time = models.DateTimeField('最后修改时间',auto_now=True)

    def __unicode__(self):
        return self.name

