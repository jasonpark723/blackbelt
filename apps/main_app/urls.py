from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^wishes$', views.home),
    url(r'^wishes/stats$', views.stats_wish),
    url(r'^wishes/new$', views.new_wish),
    url(r'^wishes/create$', views.create_wish),
    url(r'^wishes/edit/(?P<wish_id>[0-9]+)$', views.edit_wish),
    url(r'^wishes/update/(?P<wish_id>[0-9]+)$', views.update_wish),
    url(r'^wishes/delete/(?P<wish_id>[0-9]+)$', views.delete_wish),
    url(r'^wishes/granted/(?P<wish_id>[0-9]+)$', views.grant_wish),
    url(r'^wishes/like/(?P<wish_id>[0-9]+)$', views.like_wish),
]
