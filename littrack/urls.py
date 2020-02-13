from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('', include('django.contrib.auth.urls')),
    url(r'^register/$', views.register, name='register'),
    url(r'^books/$', views.my_books, name='my_books'),
    url(r'^books/add/$', views.add_book, name='add_book'),
    url(r'^books/edit/[1-9]\d*/$', views.edit_book, name='edit_book'),
    url(r'^books/edit/delete/[1-9]\d*/$', views.delete_book, name='delete_book'),
    url(r'^books/export/$', views.export_books, name='export_books'),
]
