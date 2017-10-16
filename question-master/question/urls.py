from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.start2 , name='category'),
    url(r'^login', views.login, name='category'),
    url(r'^answer/start', views.start_answer, name='answer'),
    url(r'^answer/(?P<id>\d+)/$', views.show_answer, name='answer'),
    url(r'^answer/commit', views.commit_answer, name='answer'),
    url(r'^admin', views.admin, name='answer'),
    url(r'^reg2', views.reg, name='answer'),
    url(r'^regCommit', views.regCommit, name='user'),
]