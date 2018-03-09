#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.html import strip_tags
import markdown

# Create your models here.
class Article(models.Model):
    #STATUS_CHOICES =(('d','Draft'),('p','Published'),)
    title = models.CharField('标题',max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    last_modified_time = models.DateTimeField('最后修改时间',auto_now=True)
    #文章状态这个标签暂时未用到
    #status = models.CharField('文章状态',max_length=1,choices=STATUS_CHOICES)
    abstract = models.CharField('摘要',max_length=54,blank=True,null=True,help_text="可选，如若为空将摘取正文的前54个字符")
    views = models.PositiveIntegerField('浏览数',default=0)
    likes = models.PositiveIntegerField('点赞数',default=0)
    topped = models.BooleanField('置顶',default=False)
    category = models.ForeignKey('Category',verbose_name='分类',null=True,on_delete=models.SET_NULL)
    #指定标签云(manytomany的关系)
    tag = models.ManyToManyField('Tag',verbose_name='标签集合',blank=True)

    def increase_views(self):
        self.views += 1
        #当使用save保存后才会使得阅读量增加保存到数据库
        #使用update_fields只更改views的值，可以提高效率
        self.save(update_fields=['views'])

    #保存文章摘要，复写save方法，在数据保存到数据库前进行操作
    def save(self,*args,**kwargs):
        #如果没有填写abstract，那么久自动获取正文的前54个字符作为摘要
        if not self.abstract:
            md = markdown.Markdown(extension=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            #先将Markdown文本渲染成HTML文本，利用strip_tags去掉HTML文本的全部HTML标签
            #从文本摘取前54个字符赋予给abstract
            self.abstract = strip_tags(md.convert(self.body))[:54]
        #调用父类的save方法保存到数据库中
        super(Article,self).save(*args,**kwargs)

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

class Tag(models.Model):
    name = models.CharField('标签名',max_length=20)
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间',auto_now_add=True)

    def __unicode__(self):
        return self.name
