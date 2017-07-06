from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tasks/', views.task, name='tasks'),
    url(r'^schedules/', views.schedule, name='schedules'),
]
