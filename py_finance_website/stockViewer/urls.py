from django.conf.urls import url
from stockViewer import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^help', views.help, name='help'),
]
