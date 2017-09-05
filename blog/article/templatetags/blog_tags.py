#!/usr/bin/env python
# coding=utf-8
from article.models import Article,Category
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    return Article.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_categories():
    #return Category.objects.all()
    category_list = Category.objects.annotate(num_posts=Count('article'))
    return category_list
