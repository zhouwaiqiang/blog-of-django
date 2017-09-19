"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include,handler404,handler500
from article import views
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    #url(r'^index/(?P<pk>[0-9]+)/$',views.detail,name="detail"),
    #url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[1-9]|1[0-2])/$',views.archives,name="archives"),
    url(r'^index/',include('article.urls',namespace="Article")),
    url(r'^comment/',include('comments.urls',namespace="Comment")),
]
handler404 = views.page_not_found
