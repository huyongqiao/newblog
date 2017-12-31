"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from blog import settings
from post import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^register/', views.register),
    url(r'^check_user/', views.check_user),
    url(r'^active/', views.active),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^user_info/', views.user_info),

    url(r'^post/', views.post),
    url(r'^detail/', views.detail),
    url(r'^comment/', views.comment),
    url(r'^my_articles/', views.my_articles),
    url(r'^delete_article/', views.delete_article),
    url(r'^search/', views.search),
    url(r'^add_collect/', views.add_collect),
    url(r'^my_collect/', views.my_collect),
    url(r'^del_collect/', views.del_collect),
    url(r'^upload_icon/', views.upload_icon),


    url(r'^$', views.home),
]
