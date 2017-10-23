from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<wall_user_id>\d+)/$', views.wall, name='wall'),
    url(r'^(?P<wall_user_id>\d+)/(?P<message_id>\d+)/addcomment/$', views.addcomment, name='addcomment'),
    url(r'^(?P<wall_user_id>\d+)/addmessage/$', views.addmessage, name='addmessage'),
]