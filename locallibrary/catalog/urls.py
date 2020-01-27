from django.conf.urls import url, include
from django.urls import re_path

from . import views

app_name = 'catalog'

urlpatterns = [
    url(r'^$',views.Index.as_view(), name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^authors/(?P<pk>\d+)/$', views.AuthorDetailView.as_view(), name='author_detail'),
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
    #APi Url For Book
    re_path(r'^get/$', views.APIListCreateBook.as_view(), name = 'apiBooklist'),
    re_path(r'^update/(?P<pk>\d+)/$', views.APIRetrieveUpdateDestroyBook.as_view(), name = 'apiBookUpdate'),

    re_path(r'^get/$', views.APIListCreateAuthor.as_view(), name='apiAuthorlist'),
    re_path(r'^update/(?P<pk>\d+)/$', views.APIRetrieveUpdateDestroyAuthor.as_view(), name='apiAuthorUpdate'),

    re_path(r'^get/$', views.APIListCreateBookInstances.as_view(), name='apiBookInstanceslist'),
    re_path(r'^update/(?P<pk>\d+)/$', views.APIRetrieveUpdateDestroyBookInstances.as_view(), name='apiBookInstancesUpdate'),


]