from django.urls import re_path
from facts import views

app_name = 'facts'

urlpatterns = \
    [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^days/$', views.days, name='days'),
    re_path(r'^days/rest/$', views.rest, name='rest'),
    re_path(r'^(?P<fact_id>\d+)/(?P<field>\S+)/$', views.data, name='data'),
    ]
