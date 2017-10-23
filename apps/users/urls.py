from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^create/$', views.create, name='create'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^(?P<user_id>\d+)/edit$', views.edit, name='edit'),
    url(r'^(?P<user_id>\d+)/update/$', views.update, name='update'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^new$', views.new, name='new'),
    url(r'^(?P<user_id>\d+)/destroy/$', views.destroy, name='destroy'),
    url(r'^(?P<user_id>\d+)/delete$', views.delete, name='delete'),
]
