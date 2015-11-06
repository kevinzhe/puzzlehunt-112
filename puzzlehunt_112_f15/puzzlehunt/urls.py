from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.home, name='puzzlehunt-home'),
    url(r'^p/$', views.puzzle_index, name='puzzle-index'),
    url(r'^p/(?P<puzzle_id>[0-9]+)/$', views.puzzle, name='puzzle'),
    url(r'^login$', auth_views.login, {'template_name':'login.html', 'extra_context':{'next':'/p'}}, name='login'),
]
