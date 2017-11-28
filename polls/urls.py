
from django.conf.urls import url
from django.conf.urls import include

from . import views

urlpatterns = [
#     url(r'^$', views.index, name='index'),
    url(r'^hello', views.hello, name='hello1'),
    url(r'^insert', views.insert, name='insert'),
    url(r'^read', views.read2, name='read'),
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='register'),
]
